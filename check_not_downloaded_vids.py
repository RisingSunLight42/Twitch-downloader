import os

videos = os.listdir("D:/goldberries")
ids = [file.split("_")[0] for file in videos]
print(len(ids))

file = open("twitch_urls.txt", "r")
file_content = file.read()
file.close()

all_gb_ids = []
for line in file_content.split("\n"):
    if line == "":
        continue
    goldberries_id, url = line.split("\t")
    all_gb_ids.append(goldberries_id)

for gb_id in all_gb_ids:
    if gb_id not in ids:
        print(gb_id)