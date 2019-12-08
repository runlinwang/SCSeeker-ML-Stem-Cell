from flask import render_template

def apology():
    return render_template("apology.html")
