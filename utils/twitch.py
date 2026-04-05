import requests
from pathlib import Path
from twitchdl.cache import get_cache_dir
from twitchdl.commands.download import download_one
from twitchdl.entities import Video
from twitchdl.naming import video_filename
from twitchdl.twitch import channel_videos_generator, get_video
from utils.general import DotDict

class TwitchInteraction:
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
        return new_vods


    def download_process(streamer: str, id: str, max_download_speed: int):
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
                "rate_limit": max_download_speed,
                "cache_dir": f"{get_cache_dir()}/videos/{id}/",
                "output": f"D:/vods/{streamer}" + "/{date}_{id}_{channel_login}_{title_slug}.{format}",
                "skip_live": True
            }
        )
        download_one(id, download_args)


    def get_video(video_id: str):
        return get_video(video_id)


    def video_filename(video: Video, format: str, output: str):
        return video_filename(video, format, output)


    def get_streamer_avatar(streamer_name: str):
        return requests.get(f"https://decapi.me/twitch/avatar/{streamer_name}").content.decode()
