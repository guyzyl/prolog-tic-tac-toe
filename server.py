from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    with open("index.html", "r") as f_obj:
        return f_obj.read()


@app.route("/api/make_move")
def make_move():
    # data = request.form
    return "Hey"


app.run(debug=True)
