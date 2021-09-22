import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        if not month or not day or not name:
            return "Error: name or dayor month Error" 

        if month <= 0 or  month > 12 or day <= 0 or day > 31:
            return "Error: day or month rang Wrong" 

        with sqlite3.connect("birthdays.db") as db:
            cur = db.cursor();
            cur.execute("INSERT INTO birthdays(name, month, day) values(?, ?, ?)", (name, month, day))

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        data = []
        with sqlite3.connect("birthdays.db") as db:
            cur = db.cursor();
            cur.execute("SELECT * FROM birthdays")
            data = cur.fetchall()
        return render_template("index.html", data=data)

@app.route("/edit", methods=["POST"])
def Edit():
    if request.method != "POST":
        redirect("/")

    id = request.form.get("id")
    name = request.form.get("name")
    month = int(request.form.get("month"))
    day = int(request.form.get("day"))
    if not month or not day or not name:
        return "Error: name or dayor month Error" 
    
    with sqlite3.connect("birthdays.db") as db:
        cur = db.cursor();
        cur.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", (name, month, day, id))
        
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    if request.method != "POST":
        return redirect("/")
    
    id = int(request.form.get("id"))
    if not id or id < 0:
        return "Error: id not found or id wrong"

    with sqlite3.connect("birthdays.db") as db:
        cur = db.cursor()
        cur.execute("DELETE FROM birthdays WHERE id = ?", str(id))

    return redirect("/")