"""Module providing support to read and write to the streamers.json file"""

from json import dump, load


class StreamerJsonInteraction:
    """Class providing the static methods to read and write to the streamers.json file"""

    @staticmethod
    def read_streamers_json() -> list[dict]:
        """To read the json containing the id of the last video download for x streamer."""
        with open("streamers.json", "r", newline="", encoding="UTF-8") as json_file:
            streamers_video_list = load(json_file)
        return streamers_video_list

    @staticmethod
    def write_streamers_json(streamers_video_list):
        """To write the json containing the id of the last video download for x streamer."""
        with open("streamers.json", "w", newline="", encoding="UTF-8") as json_file:
            dump(streamers_video_list, json_file)
