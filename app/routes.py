from flask import (
        Flask, render_template, redirect, url_for, request
        )

import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", songlist = model.buildSonglist())

@app.route("/new")
def addSong():
    return render_template("new_song.html")

@app.route("/save", methods = ["POST", ])
def saveSong():
    model.createSongObject(request.form)
    return redirect(url_for("index"))

@app.route("/play/<uid>")
def showSong(uid):
    song = model.displaySong(uid)
    return render_template("song.html", song = song)

@app.route("/edit/<uid>")
def edit(uid):
    song = model.editSong(uid)
    return render_template("edit_song.html",
            song = song)

@app.route("/save/<uid>", methods = ["POST", ])
def saveEditsToSong(uid):
    # move the song file from "songs/<uid>" to "songs/backup/<uid>"
    backUpSong(uid)
    # write a new file "songs/<uid>" with the contents of:
    #  - title
    #  - artist
    #  - Key
    #  - Capo
    #  - music_lyrics
    new_file_contents = createSongData(request.form)
    with open("songs/" + uid, "w") as song_file:
        song_file.write(new_file_contents)
    return redirect(url_for("index"))

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
