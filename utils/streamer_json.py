import json

class StreamerJsonInteraction:
    def read_streamers_json() -> list[dict]:
        """To read the json containing the id of the last video download for x streamer."""
        with open("streamers.json", "r", newline="") as jsonFile:
            streamers_video_list = json.load(jsonFile)
        return streamers_video_list


    def write_streamers_json(streamers_video_list):
        """To write the json containing the id of the last video download for x streamer."""
        with open("streamers.json", "w", newline="") as jsonFile:
            json.dump(streamers_video_list, jsonFile)
