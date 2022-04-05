from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
