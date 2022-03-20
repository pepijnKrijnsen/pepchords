with open("song-export.csv") as songs:
    songlist = []
    keys = [ "id", "title", "artist" ]
    lists = [ x.split(",") for x in songs ]
    for entry in lists:
        songlist.append(dict(zip(keys, entry[:3])))

songlist.pop(0)
songlist.pop(0)

for entry in songlist:
    a = entry["artist"].replace(" ","-").lower()
    t = entry["title"].replace(" ","-").lower()
    entry["url"] = a + "-" + t

with open("songlist.csv", "w") as songlist_in:
    to_write = ""
    for entry in songlist:
        to_write += entry["id"] + "," + entry["artist"] + "," + entry["title"] + "," + entry["url"] + "\n"
    songlist_in.write(to_write[:-1])
