from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    # return "hello"
    return app.send_static_file("index.html")


@app.route("/api/make_move")
def make_move():
    # data = request.form
    return "Hey"


app.run(debug=True)
