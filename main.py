import csv
from pathlib import Path
from twitchdl.commands.download import download_one
from twitchdl.cache import get_cache_dir
from twitchdl.twitch import channel_videos_generator
import requests
from time import sleep


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
    is_live = False
    for i in range(5):
        contents = requests.get('https://www.twitch.tv/' +channel_id).content.decode('utf-8')
        is_live = is_live or 'isLiveBroadcast' in contents
        if is_live:
            break
        sleep(1)
    return is_live


def get_new_vods_id(streamer: str, last_vod_downloaded_id: str) -> list[str]:
    """Get new vods id, list returned is sort by older to newer."""
    last_vod_downloaded_id = int(last_vod_downloaded_id)
    _, generator = channel_videos_generator(channel_id=streamer, max_videos=40, sort="time", type="archive")
    videos = list(generator)
    is_live = is_streamer_live(streamer)
    if is_live:
        videos.pop(0)
    new_vods = []
    for video in videos:
        if int(video["id"]) == last_vod_downloaded_id:
            break
        new_vods.insert(0, video["id"])
    print(new_vods, streamer, is_live)
    return new_vods


def download_process(streamer: str, id: str):
    """Download the given vod id, in the streamer folder."""
    Path(f"vods/{streamer}").mkdir(parents=True, exist_ok=True)
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
                    "cache_dir": f"{get_cache_dir()}/videos/{id}/",
                    "output": f"vods/{streamer}" + "/{date}_{id}_{channel_login}_{title_slug}.{format}",
                }
            )
    download_one(id, download_args)


def write_streamers_csv(streamers_video_list):
    """To write the CSV containing the id of the last video download for x streamer."""
    with open("streamers.csv", "w", newline="") as csvFile:
        fieldnames = ['streamer', 'video_id']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(streamers_video_list)


if __name__ == "__main__":
    streamers_video_list = read_streamers_csv()
    for streamer in streamers_video_list:
        new_vods = get_new_vods_id(streamer["streamer"], streamer["video_id"])
        for new_vod in new_vods:
            download_process(streamer["streamer"], new_vod)
            streamer["video_id"] = new_vod
            write_streamers_csv(streamers_video_list)
