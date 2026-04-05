import csv

class StreamerCSVInteraction:
    def read_streamers_csv() -> list[dict]:
        """To read the CSV containing the id of the last video download for x streamer."""
        with open("streamers.csv", "r", newline="") as csvFile:
            reader = csv.DictReader(csvFile)
            streamers_video_list = [row for row in reader]
        return streamers_video_list


    def write_streamers_csv(streamers_video_list):
        """To write the CSV containing the id of the last video download for x streamer."""
        with open("streamers.csv", "w", newline="") as csvFile:
            fieldnames = ['streamer', 'video_id', 'webhook_url']
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(streamers_video_list)
