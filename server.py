import os

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import data_handler

UPLOAD_FOLDER = './sample_data/images'
ALLOWED_EXTENSIONS = {'jpg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(12).hex()


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
    if request.method == 'POST':
        data = {'title': request.form.get('title', default="not provided"),
                'message': request.form.get('message', default="not provided"),
                'image': upload_image()}
        # TODO for other endpoint form processing data
        new_question = data_handler.save_new_question_data(data)
        new_question_id = new_question['id']
        return redirect('/question/' + new_question_id)


@app.route("/question/<id>/delete")
def delete_question(id):
    # Delete question image
    question_data = data_handler.get_question(id)
    image_delete_from_server(question_data)
    # Delete answer images
    answers = data_handler.get_answer_for_question(id)
    if answers:
        for answer in answers:
            image_delete_from_server(answer)
            data_handler.delete_answer(answer.get('id'))
    data_handler.delete_question(id)
    return redirect("/")


@app.route('/answer/<id>/delete', methods=['POST'])
def delete_answer(id):
    question_id = request.form['question_id']
    answer_list = data_handler.get_answers()
    for answer in answer_list:
        if answer['id'] == str(id):
            image_delete_from_server(answer)
    data_handler.delete_answer(id)
    return redirect('/question/' + question_id)


def image_delete_from_server(item):
    if item['image'] != '':
        try:
            url_path = item['image']
            filename = url_path[len('/uploads/'):]
            filepath = UPLOAD_FOLDER + "/" + filename
            if os.path.exists(filepath):
                os.remove(filepath)
        except ValueError:
            print("File doesn't exist")


@app.route('/question/<id>')
def display_question(id):
    question = data_handler.get_question(id)
    data_handler.increase_question_view_count(question)
    question = data_handler.convert_to_datetime(question)
    answers = data_handler.convert_to_datetime(data_handler.get_answer_for_question(id))
    return render_template('question.html', question=question, answers=answers)


@app.route("/question/<id>/edit", methods=['GET', 'POST'])
def edit_question(id):
    question = data_handler.get_question(id)
    if request.method == 'GET':
        return render_template('edit-question.html', question=question)
    elif request.method == 'POST':
        file = request.files['file']
        if file.filename != "":
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # src = url_for('uploaded_file', filename=filename)
            # if src == question['image']:
            updated_dict = {'id': id, 'title': request.form['title'], 'message': request.form['message'],
                            'image': question['image']}
            data_handler.edit_question(updated_dict)
        else:
            # Delete old image --- refactor --- change to function
            if question['image'] != "":
                url_path = question['image']
                filename = url_path[len('/uploads/'):]
                os.remove(UPLOAD_FOLDER + "/" + filename)
            updated_dict = {'id': id, 'title': request.form['title'], 'message': request.form['message'],
                            'image': None}
            data_handler.edit_question(updated_dict)
        return redirect('/question/' + id)


@app.route('/question/<id>/new-answer', methods=['GET', 'POST'])
def add_answer(id):
    if request.method == 'GET':
        answers = data_handler.get_answer_for_question(id)
        answers = data_handler.convert_to_datetime(answers)
        return render_template('add-answer.html', question=data_handler.get_question(id), answers=answers)
    elif request.method == 'POST': # refactor for hackers
        answer_data = {'message': request.form['message'], 'question_id': request.form['question_id'],
                       'image': upload_image()}
        data_handler.save_answer_data(answer_data)
        return redirect('/question/' + id)


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def q_upvote(question_id):
    question_dict = data_handler.get_question(question_id)
    data_handler.increase_question_vote(question_dict)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def a_upvote(answer_id):
    answers = data_handler.get_answers()
    # data_handler.get_answer_for_question(id)
    for answer in answers:
        if str(answer_id) == answer['id']:
            data_handler.increase_answer_vote(answer)
            return redirect('/question/' + answer['question_id'])


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def q_downvote(question_id):
    question_dict = data_handler.get_question(question_id)
    data_handler.decrease_question_vote(question_dict)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def a_downvote(answer_id):
    answers = data_handler.get_answers()
    for answer in answers:
        if str(answer_id) == answer['id']:
            data_handler.decrease_answer_vote(answer)
            q_id = answer['question_id']
            return redirect('/question/' + q_id)


# Below are functions for uploading an image


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return None
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return url_for('uploaded_file', filename=filename)
    return ''' <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method="post" action="/upload-image" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
        '''


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
