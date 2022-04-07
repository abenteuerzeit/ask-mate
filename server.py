from flask import Flask, render_template
import data_handler
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    questions = data_handler.get_question_data()
    return render_template('list.html', questions=questions)


@app.route("/add-question")
def route_add_question():
    add = data_handler.save_question_data()
    return render_template('add-question.html', add=add)


# @app.route("/question/<id>/edit")
# def edit_question(id):
#     return render_template('edit-question.html')

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )