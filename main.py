from utils.discord import DiscordInteraction
from utils.general import StdoutWrapper, EnvManager
from utils.streamer_json import StreamerJsonInteraction
from utils.twitch import TwitchInteraction
from pathlib import Path
from datetime import datetime, timezone
from contextlib import redirect_stdout


if __name__ == "__main__":
    env_manager = EnvManager()
    streamers_video_list = StreamerJsonInteraction.read_streamers_json()
    number_of_streamers = len(streamers_video_list)
    DiscordInteraction.send_webhook(
        f"The download script is starting, {len(streamers_video_list)} streamers loaded.", [env_manager.WEBHOOK_URL],
        "https://pbs.twimg.com/profile_images/1938396805336563712/Wihg-eQ-_400x400.jpg"
    )
    for streamer_index, streamer in enumerate(streamers_video_list):
        streamer_name = streamer["streamer"]
        new_vods = TwitchInteraction.get_new_vods_id(streamer_name, streamer["video_id"])
        avatar_url = TwitchInteraction.get_streamer_avatar(streamer_name)
        webhook_urls = [env_manager.WEBHOOK_URL] + streamer["webhook_urls"]
        streamer_folder = f"{env_manager.DOWNLOAD_PATH}{streamer_name}"
        Path(streamer_folder).mkdir(parents=True, exist_ok=True)
        output_path = streamer_folder + "/{date}_{id}_{channel_login}_{title_slug}.{format}"
        if len(new_vods) == 0:
            DiscordInteraction.send_webhook(
                f"No VODs to download yet for **{streamer_name}**. ({streamer_index+1}/{number_of_streamers})",
                [env_manager.WEBHOOK_URL],
                avatar_url,
            )
        for index, new_vod in enumerate(new_vods):
            video_infos = TwitchInteraction.get_video(new_vod)
            file_path = TwitchInteraction.video_filename(video_infos, "mp4", output_path)
            starting_date = datetime.now(timezone.utc)
            webhooks = DiscordInteraction.send_webhook_starting_download(
                f"Streamer {streamer_index+1}/{number_of_streamers}" , index, len(new_vods), avatar_url, video_infos, webhook_urls
            )

            stream = StdoutWrapper(webhooks, index, len(new_vods), avatar_url, video_infos)
            with redirect_stdout(stream):
                TwitchInteraction.download_process(streamer_name, new_vod, env_manager.MAX_DOWNLOAD_SPEED, output_path)

            if not stream.has_been_skipped:
                streamer["video_id"] = new_vod
                StreamerJsonInteraction.write_streamers_json(streamers_video_list)

            ending_date = datetime.now(timezone.utc)
            time_elapsed= ending_date - starting_date
            for webhook in webhooks:
                DiscordInteraction.send_webhook_ending_download(webhook, index, len(new_vods), avatar_url, video_infos, file_path, time_elapsed, stream.has_been_skipped)

    DiscordInteraction.send_webhook(
        "Download script has ended.",
        [env_manager.WEBHOOK_URL],
        "https://pbs.twimg.com/profile_images/1938396805336563712/Wihg-eQ-_400x400.jpg"
    )
