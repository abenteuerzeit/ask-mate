from flask import Flask, render_template, request, redirect

import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    # / list?order_by = title & order_direction = desc
    order_by = request.args.get('order_by', 'id')
    order_direction = request.args.get('order_direction', 'desc')
    questions = data_handler.get_questions()
    questions = data_handler.convert_to_datetime(questions)
    questions.sort(key=lambda question: question[order_by], reverse=(order_direction == 'desc'))
    return render_template("list.html", questions=questions, order_by=order_by, order_direction=order_direction)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add-question.html")
    data = {'title': request.form['title'], 'message': request.form['message'], 'image': 'None'}
    new_question = data_handler.save_new_question_data(data)
    new_question_id = new_question['id']
    return redirect('/question/' + new_question_id)


@app.route("/question/<id>/delete")
def delete_question(id):
    if request.method == "GET":
        data_handler.delete_question(id)
    return redirect("/")


@app.route('/question/<id>')
def display_question(id):
    if request.method == "GET":
        question = data_handler.get_question(id)
        data_handler.increase_view_count(question)
        question = data_handler.convert_to_datetime(question)
        answers = data_handler.convert_to_datetime(data_handler.get_answer_for_question(id))
        return render_template('question.html', question=question, answers=answers)


# @app.route("/question/<id>/edit")
# def edit_question(id):
#     return render_template('edit-question.html')


@app.route('/question/<id>/new-answer', methods=['GET', 'POST'])
def add_answer(id):
    if request.method == 'GET':
        answers = data_handler.get_answer_for_question(id)
        answers = data_handler.convert_to_datetime(answers)
        return render_template('add-answer.html', question=data_handler.get_question(id), answers=answers)
    elif request.method == 'POST':
        answer_data = {'message': request.form['message'], 'question_id': request.form['question_id'], 'image': None}
        new_answer_id = data_handler.save_answer_data(answer_data)
        print(new_answer_id)
        return redirect('/question/' + id)


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def q_upvote(question_id):
    if request.method == 'POST':
        question_dict = data_handler.get_question(question_id)
        data_handler.increase_question_vote(question_dict)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def a_upvote(answer_id):
    if request.method == 'POST':
        answers = data_handler.get_answers()
        for answer in answers:
            if str(answer_id) == answer['id']:
                data_handler.increase_answer_vote(answer)
                q_id = answer['question_id']
                return redirect('/question/' + q_id)


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def q_downvote(question_id):
    if request.method == 'POST':
        question_dict = data_handler.get_question(question_id)
        data_handler.decrease_question_vote(question_dict)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def a_downvote(answer_id):
    if request.method == 'POST':
        answers = data_handler.get_answers()
        for answer in answers:
            if str(answer_id) == answer['id']:
                data_handler.decrease_answer_vote(answer)
                q_id = answer['question_id']
                return redirect('/question/' + q_id)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
