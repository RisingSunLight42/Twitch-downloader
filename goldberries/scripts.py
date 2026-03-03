import os

def download_goldberries(twitch_id: str, goldberries_id: str):
    os.system("twitch-dl download -w 20 -f mp4 --output D:/goldberries/" + goldberries_id + "_{date}_{id}_{channel_login}_{title_slug}.{format} " + twitch_id)

def goldberries_script():
    file = open("./goldberries/twitch_urls_past_20_03_2025.txt", "r")
    file_content = file.read()
    file.close()

    videos = os.listdir("D:/goldberries")
    ids = [file.split("_")[0] for file in videos]

    for line in file_content.split("\n"):
        if line == "":
            continue
        goldberries_id, challenge_id, url, date = line.split("\t")
        if goldberries_id in ids:
            print("Skipping "+goldberries_id+" (already done)")
            continue
        twitch_id = url.split("/")[-1].split("?")[0]
        download_goldberries(twitch_id, goldberries_id)
        with open("twitch_done.txt", "a", encoding="utf-8") as file:
            file.write(goldberries_id + " done " + "\n")
        print(goldberries_id, " ", twitch_id)

goldberries_script()