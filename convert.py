import os

# USE twitch-dl python package for auto download https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows
def download_vod(twitch_id: str):
    os.system("twitch-dl download -q source -w 10 -f mp4 --output C:/Users/sunli/Documents/code/python/downloadTwitch/toconvert/{date}_{id}_{channel_login}_{title_slug}.{format} " + twitch_id)


download_vod("2486760617")
