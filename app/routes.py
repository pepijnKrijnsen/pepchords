from flask import (
        Flask, render_template, redirect, url_for, request
        )

import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", songlist = model.buildSonglist())

@app.route("/song/new")
def addSong():
    return render_template("new_song.html")

@app.route("/song/save", methods = ["POST", ])
def saveSong():
    if not request.form["title"] or not request.form["artist"]:
        return redirect(url_for("addSong"))
    model.createSongObject(request.form)
    return redirect(url_for("index"))

@app.route("/song/play/<uid>")
def showSong(uid):
    song = model.displaySong(uid)
    return render_template("song.html", song = song)

@app.route("/song/edit/<uid>")
def edit(uid):
    song = model.editSong(uid)
    return render_template("edit_song.html", song = song)

@app.route("/zoom/save/<uid>")
def saveZoomLevel(uid):
    if request.args.get("fontchange"):
        model.updateFontSize(uid, int(request.args.get("fontchange")))
    return redirect(url_for("index"))

@app.route("/practice")
def logPractice():
    return render_template("practice.html", 
            practice_types = getPracticeTypes())

@app.route("/practice/save", methods = ["POST", ])
def savePracticeLog():
    # persistence!
    return redirect(url_for("index"))
