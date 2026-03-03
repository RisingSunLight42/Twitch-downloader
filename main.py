import csv
import requests
import os
from pathlib import Path
from twitchdl.commands.download import download_one
from twitchdl.cache import get_cache_dir
from twitchdl.utils import format_time
from twitchdl.twitch import channel_videos_generator, get_video
from twitchdl.naming import video_filename
from twitchdl.entities import Video
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# idée amélioration : afficher les stats des VODs à DL (nombre, total de GB, total de durée...)
# faire blacklist de certains mots dans les titres pour skip certaines vods inutiles (combo whitelist de streamers où on veut
# tout DL anyway)
class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def read_streamers_csv() -> list[dict]:
    """To read the CSV containing the id of the last video download for x streamer."""
    with open("streamers.csv", "r", newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        streamers_video_list = [row for row in reader]
    return streamers_video_list


def is_streamer_live(channel_id: str) -> bool:
    """Check if given streamer is currently live."""
    content = requests.get("https://decapi.me/twitch/uptime/" + channel_id + "?offline_msg=off").content.decode("utf-8")
    return not "off" in content


def get_new_vods_id(streamer: str, last_vod_downloaded_id: str) -> list[str]:
    """Get new vods id, list returned is sort by older to newer."""
    last_vod_downloaded_id = int(last_vod_downloaded_id)
    _, generator = channel_videos_generator(channel_id=streamer, max_videos=40, sort="time", type="archive")
    videos = list(generator)
    new_vods = []
    for video in videos:
        if int(video["id"]) <= int(last_vod_downloaded_id):
            break
        new_vods.insert(0, video["id"])
    if len(new_vods) == 0:
        return []
    is_live = is_streamer_live(streamer)
    if is_live:
        new_vods.pop()
    return new_vods


def download_process(streamer: str, id: str):
    """Download the given vod id, in the streamer folder."""
    Path(f"D:/vods/{streamer}").mkdir(parents=True, exist_ok=True)
    download_args = DotDict(
        {
            "format": "mp4",
            "keep": False,
            "quality": "source",
            "max_workers": 20,
            "no_join": False,
            "overwrite": True,
            "start": None,
            "end": None,
            "rate_limit": int(os.environ.get("MAX_DOWNLOAD_SPEED")),
            "cache_dir": f"{get_cache_dir()}/videos/{id}/",
            "output": f"D:/vods/{streamer}" + "/{date}_{id}_{channel_login}_{title_slug}.{format}",
        }
    )
    download_one(id, download_args)


def write_streamers_csv(streamers_video_list):
    """To write the CSV containing the id of the last video download for x streamer."""
    with open("streamers.csv", "w", newline="") as csvFile:
        fieldnames = ['streamer', 'video_id', 'webhook_url']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(streamers_video_list)


def send_webhook(content: str, webhook_urls: list, avatar_url: str = "", embed: DiscordEmbed = None) -> list[DiscordWebhook]:
    webhooks = []
    for webhook_url in webhook_urls:
        webhook = DiscordWebhook(
            url=webhook_url,
            content=content,
            avatar_url=avatar_url
        )
        if embed is not None:
            webhook.add_embed(embed)
        webhook.execute()
        webhooks.append(webhook)
    return webhooks


def send_webhook_starting_download(content: str, vod_index: int, vod_number: int, avatar_url: str, video_infos: Video, webhook_urls: list):
    embed = DiscordEmbed(title=f"Download in progress (VOD {vod_index+1}/{vod_number})", color="3498db")
    embed.set_author(video_infos["creator"]["displayName"], icon_url=avatar_url)
    embed.add_embed_field(name="Title", value=video_infos["title"], inline=False)
    embed.add_embed_field(name="Game", value=video_infos["game"]["name"], inline=False)
    embed.add_embed_field(name="Date published", value=video_infos["publishedAt"].replace("T"," ").replace("Z", ""))
    embed.add_embed_field(name="Length", value=format_time(video_infos["lengthSeconds"]), inline=False)
    embed.set_footer(text=f"VOD id: {video_infos["id"]}")
    embed.set_timestamp()
    return send_webhook(content, webhook_urls, avatar_url, embed)


def send_webhook_ending_download(
        webhook: DiscordWebhook,
        vod_index: int,
        vod_number: int,
        avatar_url: str,
        video_infos: Video,
        file_path: str,
        time_elapsed: timedelta
    ):
    embed = DiscordEmbed(title=f"Download successful (VOD {vod_index+1}/{vod_number})", color="57f287")
    embed.set_author(video_infos["creator"]["displayName"], icon_url=avatar_url)
    embed.add_embed_field(name="Title", value=video_infos["title"], inline=False)
    embed.add_embed_field(name="Game", value=video_infos["game"]["name"], inline=False)
    embed.add_embed_field(name="Date published", value=video_infos["publishedAt"].replace("T"," ").replace("Z", ""))
    embed.add_embed_field(name="Length", value=format_time(video_infos["lengthSeconds"]), inline=False)
    embed.add_embed_field(name="File size", value=f"{os.path.getsize(file_path)/(1<<30):,.0f} GB")
    embed.add_embed_field(name="Time elapsed", value=f"{time_elapsed}")
    embed.set_footer(text=f"VOD id: {video_infos["id"]}")
    embed.set_timestamp()
    webhook.remove_embeds()
    webhook.add_embed(embed)
    webhook.edit()

if __name__ == "__main__":
    load_dotenv()
    streamers_video_list = read_streamers_csv()
    number_of_streamers = len(streamers_video_list)
    send_webhook(
        f"The download script is starting, {len(streamers_video_list)} streamers loaded.", [os.environ.get("WEBHOOK_URL")],
        "https://pbs.twimg.com/profile_images/1938396805336563712/Wihg-eQ-_400x400.jpg"
    )
    for streamer_index, streamer in enumerate(streamers_video_list):
        streamer_name = streamer["streamer"]
        new_vods = get_new_vods_id(streamer_name, streamer["video_id"])
        avatar_url = requests.get(f"https://decapi.me/twitch/avatar/{streamer_name}").content.decode()
        webhook_urls = [os.environ.get("WEBHOOK_URL"), streamer["webhook_url"]] if len(streamer["webhook_url"]) != 0 else [os.environ.get("WEBHOOK_URL")]
        if len(new_vods) == 0:
            send_webhook(
                f"No VODs to download yet{
                    f", but **{streamer_name}** is currently live. ({streamer_index+1}/{number_of_streamers})" if is_streamer_live(streamer_name) 
                    else f" for **{streamer_name}**. ({streamer_index+1}/{number_of_streamers})"
                }",
                [os.environ.get("WEBHOOK_URL")],
                avatar_url,
            )
        for index, new_vod in enumerate(new_vods):
            video_infos = get_video(new_vod)
            file_path = video_filename(video_infos, "mp4", f"D:/vods/{streamer_name}" + "/{date}_{id}_{channel_login}_{title_slug}.{format}")
            starting_date = datetime.now(timezone.utc)
            webhooks = send_webhook_starting_download(
                f"Streamer {streamer_index+1}/{number_of_streamers}" , index, len(new_vods), avatar_url, video_infos, webhook_urls
            )

            download_process(streamer_name, new_vod)

            streamer["video_id"] = new_vod
            write_streamers_csv(streamers_video_list)

            ending_date = datetime.now(timezone.utc)
            time_elapsed= ending_date - starting_date
            for webhook in webhooks:
                send_webhook_ending_download(webhook, index, len(new_vods), avatar_url, video_infos, file_path, time_elapsed)
    send_webhook(
        "Download script has ended.",
        [os.environ.get("WEBHOOK_URL")],
        "https://pbs.twimg.com/profile_images/1938396805336563712/Wihg-eQ-_400x400.jpg"
    )
