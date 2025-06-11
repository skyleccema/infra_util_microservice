from flask import Flask, make_response

app = Flask(__name__)

def hello():
    return "Hello vov"

@app.route("/")
def hello_world():
    return make_response(hello())