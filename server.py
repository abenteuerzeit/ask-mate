from flask import Flask, render_template

import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    questions = data_handler.get_question_data()
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run()
