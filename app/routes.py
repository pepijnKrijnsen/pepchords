from flask import (
        Flask, render_template, redirect, url_for, request
        )

import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", songlist = model.buildSonglist())

@app.route("/song/new", methods = ["GET", "POST"])
def addSong():
    if request.method == "GET":
        return render_template("new_song.html")
    else:
        error = model.checkForArtistAndTitle(request.form)
        if not error:
            model.createAndPersistSongStrings(request.form)
            return redirect(url_for("index"))
        else:
            flash(error)

@app.route("/song/play/<uid>")
def showSong(uid):
    song = model.getSongObject(uid)
    return render_template("song.html", song = song)

@app.route("/song/edit/<uid>", methods = ["GET", "POST"])
def editSong(uid):
    song = model.editSong(uid)
    if request.method == "GET":
        return render_template("edit_song.html", song = song)
    else:
        error = model.checkForArtistAndTitle(request.form)
        if not error:
            model.createAndPersistSongStrings(request.form)
            return redirect(url_for("showSong", uid = song["uid"]))
        else:
            flash(error)

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
