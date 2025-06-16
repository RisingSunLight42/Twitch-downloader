import os
from twitchdl.commands.download import download
from twitchdl.cache import get_cache_dir

# USE twitch-dl python package for auto download https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows
def download_vod(twitch_id: str):
    os.system("twitch-dl download -q source -w 10 -f mp4 --output C:/Users/sunli/Documents/code/python/downloadTwitch/toconvert/{date}_{id}_{channel_login}_{title_slug}.{format} " + twitch_id)

class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

id = "2486760617"

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
                "output": "{date}_{id}_{channel_login}_{title_slug}.{format}",
            }
        )
download([id], download_args)
