from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def greet():
    if not request.form.get("name"):
        return "failure"
    return "success"
    return render_template("greet.html", name=name)
