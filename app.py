from flask import (
        Flask, render_template, redirect, url_for, request
        )

from model import (
        buildSonglist, findSong, createNewSong, parseSong
        )

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", songlist = buildSonglist())

@app.route("/play/<uid>")
def getSong(uid):
    song_object = findSong(uid)
    if song_object:
        # read the song file and create a dictionary
        song = parseSong(song_object)
        song["url"] = uid
        return render_template("song.html", song = song)
    else:
        # create a new song file
        createNewSong(uid)
        return redirect(url_for("index"))

@app.route("/edit/<uid>")
def edit(uid):
    song = parseSong(findSong(uid))
    return render_template("song_attributes.html",
                        song = song)

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


def newSongToCsv():
    pass

def getPracticeTypes():
    types = [ "", "stream", "repetition", "new song" ]
    return types
