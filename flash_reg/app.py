from flask import Flask, render_template, request

app = Flask(__name__)

SPORT = ["Basketball", "Soccer", "Ultimate Frisbee"]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORT)

@app.route("/register", methods=["POST"])
def greet():
    if not request.form.get("name") or request.form.get("sport") not in SPORT:
        return render_template("fail.html")
    return render_template("success.html")
