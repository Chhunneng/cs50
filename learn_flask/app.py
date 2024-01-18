from flask import Flask, render_templates, request

app = Flask(__name__)

@app.route("/")
def index():
    
