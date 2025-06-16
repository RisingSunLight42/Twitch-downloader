import csv
from twitchdl.commands.download import download
from twitchdl.cache import get_cache_dir
from twitchdl.twitch import channel_videos_generator


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


'''
File with streamers: channel_name and last video id downloaded.
Then, go for each streamers:
    check the last videos, check if any is new
    download every new videos -> one folder for each streamer
update the file with the idea
'''

def read_streamers_csv() -> list[dict]:
    """To read the CSV containing the id of the last video download for x streamer."""
    with open("streamers.csv", "r", newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        streamers_video_list = [row for row in reader]
    return streamers_video_list


def download_process():
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
                    "output": "vods/{date}_{id}_{channel_login}_{title_slug}.{format}",
                }
            )
    download([id], download_args)


if __name__ == "__main__":
    streamers_video_list = read_streamers_csv()
    print(streamers_video_list)

# total_count, generator = channel_videos_generator(channel_id="lumi_pomme", max_videos=40, sort="time", type="archive")
# print(total_count)
# print(list(generator))
