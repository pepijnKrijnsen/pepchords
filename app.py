from flask import (
        Flask, render_template, redirect, url_for, request
        )

from model import (
        buildSonglist, findSong, createNewSong
        )

app = Flask(__name__)

@app.route("/")
def index():
    practice_sessions = [
            {
                "type": "Repetition",
                "start": 48000,
                "end": 48600,
                "duration": 600
                },
            {
                "type": "Stream",
                "start": 36000,
                "end": 43200,
                "duration": 3600
                }
            ]
    return render_template("index.html", 
            songlist = buildSonglist(), 
            practice_sessions = practice_sessions)

@app.route("/play/<uid>")
def getSong(uid):
    song_object = findSong(uid)
    if song_object[:5] == "songs":
        createNewSong(song_object)
        return redirect(url_for("index"))
    else:
        # read the song file and create a dictionary
        song = parseSong(song_object)
        song["url"] = uid
        return render_template("song.html", song = song)

@app.route("/edit/<uid>")
def edit(uid):
    return render_template("song_attributes.html",
            song_data = getSongData(uid))

@app.route("/song/new")
def addNewSong():
    return render_template("song_attributes.html")

@app.route("/song/save", methods = ["POST", ])
def saveNewSong():
    line = request.form["title"] + "," + request.form["artist"] + ",,,,,," + request.form["key"] + "," + request.form["capo"] + ",,0,false" + "\n"
    with open("newsongs.csv", "a") as f:
        f.write(line)
    return redirect(url_for("index"))

@app.route("/practice")
def logPractice():
    return render_template("practice.html", 
            practice_types = getPracticeTypes())

@app.route("/practice/save", methods = ["POST", ])
def savePracticeLog():
    # persistence!
    return redirect(url_for("index"))

def parseSong(songObject):
    items = songObject.split("\n\n")
    song = dict()
    keys = ["title", "artist", "metadata"]
    for k in keys:
        song[k] = items.pop(0)
    song["metadata"] = song["metadata"].split("\n")
    song["chords_lyrics"] = [ x.split("\n") for x in items ]
    return song

def newSongToCsv():
    pass

def getPracticeTypes():
    types = [ "", "stream", "repetition", "new song" ]
    return types
