from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def greet():
    if "name" not in request.form
    name = request.form.get("name", "world")
    return render_template("greet.html", name=name)
