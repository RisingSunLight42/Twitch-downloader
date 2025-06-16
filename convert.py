import os
import ffmpeg

# USE twitch-dl python package for auto download https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows
# https://www.youtube.com/watch?v=eq-mjehACe4 auto upload on youtube

def download_vod(twitch_id: str):
    os.system("twitch-dl download -q source -w 10 -f mp4 --output C:/Users/sunli/Documents/code/python/downloadTwitch/toconvert/{date}_{id}_{channel_login}_{title_slug}.{format} " + twitch_id)


def download_goldberries(twitch_id: str, goldberries_id: str):
    os.system("twitch-dl download -q 720p -w 10 -f mp4 --output D:/goldberries/" + goldberries_id + "_{date}_{id}_{channel_login}_{title_slug}.{format} " + twitch_id)


def convert_to_mp4(m4v_file: str):
    name, ext = os.path.splitext(m4v_file)
    out_name = r"converted\\" + name.replace("toconvert\\", "") + ".mp4"
    ffmpeg.input(m4v_file).output(out_name).run()
    print("Finished converting {}".format(m4v_file))


def convert_all(start_dir: str):
    for path, folder, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.mkv'):
                print("Found file: %s" % file)
                convert_to_mp4(os.path.join(start_dir, file))
            else:
                pass


def goldberries_script():
    file = open("twitch_urls.txt", "r")
    file_content = file.read()
    file.close()

    videos = os.listdir("D:/goldberries")
    # ids = [file.split("_")[0] for file in videos]

    for line in file_content.split("\n"):
        if line == "":
            continue
        goldberries_id, url = line.split("\t")
        # if goldberries_id in ids:
            # continue
        twitch_id = line.split("/")[-1].split("?")[0]
        download_goldberries(twitch_id, goldberries_id)
        with open("twitch_done.txt", "a", encoding="utf-8") as file:
            file.write(goldberries_id + " done " + "\n")
        print(goldberries_id, " ", twitch_id)


download_vod("2486760617")

# goldberries_script()