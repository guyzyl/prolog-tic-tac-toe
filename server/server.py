from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Wrold!"


@app.route("/api/make_move", methods=["POST"])
def make_move():
    # data = request.form
    return "Hey"


app.run()
