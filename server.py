import fnmatch
import os

import bcrypt
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename

import db_data_handler
from bonus_questions import SAMPLE_QUESTIONS

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'jpg', 'png'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(12).hex()


@app.route("/list")
@app.route('/search')
@app.route("/")
def list_questions():
    order_by, order_direction = request.args.get('order_by', 'id'), request.args.get('order_direction', 'desc')
    if 'asc' in order_by:
        order_by, order_direction = order_by[:-len('-asc')], 'asc'
    db_questions = db_data_handler.get_questions()
    db_questions.sort(key=lambda question: question[order_by], reverse=(order_direction == 'desc'))

    search_results = db_data_handler.search(request.args.get('q'))

    is_logged_in = False
    if "username" in session:
        is_logged_in = True

    return render_template("list.html", questions=db_questions,
                           order_by=order_by, order_direction=order_direction,
                           results=search_results,
                           tags=db_data_handler.get_tags(), question_tags=db_data_handler.get_question_tags(),
                           is_logged_in=is_logged_in,
                           username=session.get("username")
                           )


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        username = request.form.get("username")
        password = bcrypt.hashpw((request.form.get("password")).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        registration_data = dict()
        registration_data['username'] = username
        registration_data['password'] = password
        registration_data['date'] = db_data_handler.NOW
        db_data_handler.register_user(registration_data)
        return redirect(url_for('list_questions'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_hash = db_data_handler.users(username)  # TODO SQL users table; SELECT WHERE username
        if user_hash is not None:
            if bcrypt.checkpw(password.encode('utf-8'), user_hash['passwordhash'].encode('utf-8')):
                session["username"] = username
                return redirect(url_for("list_questions"))
        session["bad_login_or_password"] = True
    return render_template('login.html', status=session.get("bad_login_or_password", default=False))


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for("list_questions"))


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route('/question/<question_id>', methods=['GET'])
def display_question(question_id):
    question, answers = db_data_handler.get_question(question_id), db_data_handler.get_answer_for_question(question_id)
    db_data_handler.increase_question_view_count(question['id'])
    if request.method == 'GET':
        return render_template('question.html', question=question, answers=answers,
                               tags=db_data_handler.get_tags(),
                               question_tags=db_data_handler.get_question_tag_ids(question_id))
    return question, answers


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add-question.html")
    if request.method == 'POST':
        new_question = db_data_handler.save_new_question_data({
            'title': request.form.get('title', default="not provided"),
            'message': request.form.get('message', default="not provided"),
            'image': upload_image()})
        return redirect('/question/' + str(new_question['id']))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    image_delete_from_server(db_data_handler.get_question(question_id))
    answers, tags = db_data_handler.get_answer_for_question(question_id), db_data_handler.get_question_tag_ids(id)
    if tags:
        for tag in tags:
            db_data_handler.delete_tag_from_question(question_id, tag.get('tag_id'))
    if answers:
        for answer in answers:
            image_delete_from_server(answer)
            comments = db_data_handler.get_comment_for_answer(answer.get('id'))
            for comment in comments:
                db_data_handler.delete_comment(comment.get('id'))
            db_data_handler.delete_answer(answer.get('id'))
    db_data_handler.delete_question_comment(question_id)
    db_data_handler.delete_question(question_id)
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question = db_data_handler.get_question(question_id)
    tag_ids, tags = db_data_handler.get_question_tag_ids(question_id), db_data_handler.get_tags()
    if request.method == 'GET':
        return render_template('edit-question.html', question=question, tag_ids=tag_ids, tags=tags)
    elif request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = save_image(file)
            filepath = url_for('uploaded_file', filename=filename)
            question['image'] = filepath
        db_data_handler.edit_question({'id': question_id,
                                       'title': request.form.get('title'),
                                       'message': request.form.get('message'),
                                       'image': question['image']})
        return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    question = db_data_handler.get_question(question_id)
    if request.method == 'GET':
        question_tags = db_data_handler.get_question_tag_ids(question_id)
        return render_template('add-tag.html', question=question,
                               tags=db_data_handler.get_tags(),
                               question_tags=question_tags)
    elif request.method == 'POST':
        tag_id, name = request.form.get('tag'), request.form.get('add_tag')
        if name:
            db_data_handler.create_new_tag(name)
            tag_id = db_data_handler.get_tag_id(name)
            tag_id = tag_id.get('id')
        db_data_handler.assign_tag_to_question(id, tag_id)
        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag_from_question(question_id, tag_id):
    db_data_handler.delete_tag_from_question(question_id, tag_id)
    return redirect(f'/question/{question_id}')


# ------------------- ANSWERS ---------------------- #
@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        question = db_data_handler.get_question(question_id)
        answers = db_data_handler.get_answer_for_question(question_id)
        question['id'] = str(question.get('id'))
        return render_template('add-answer.html', question=question, answers=answers)
    elif request.method == 'POST':
        db_data_handler.save_answer_data({'message': request.form.get('message'), 'question_id': question_id,
                                          'image': upload_image()})
        return redirect('/question/' + question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id, answer_list = request.args.get('question_id'), db_data_handler.get_answers()
    for answer in answer_list:
        if str(answer['id']) == answer_id:
            image_delete_from_server(answer)
    db_data_handler.delete_answer(answer_id)
    return redirect('/question/' + question_id)


# ------------------- COMMENTS ---------------------- #
@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment(question_id):
    if request.method == 'GET':
        comments = db_data_handler.get_comment_for_question(question_id)
        return render_template('new-comment.html',
                               question=db_data_handler.get_question(question_id),
                               comments=comments)
    elif request.method == 'POST':
        # file = request.files['file']
        # if file.filename != "" and not allowed_file(file.filename):
        #     error = display_error_message(question_id)
        #     return render_template('error.html', error=error, is_comment=True)
        comment_data = {'message': request.form.get('message'), 'answer_id': question_id,
                        'image': upload_image()}
        db_data_handler.save_new_comment(comment_data)
        return redirect('question' + question_id)


# ------------------- VOTES ---------------------- #
@app.route('/question/<question_id>/vote-up')
def increase_question_vote(question_id):
    db_data_handler.increase_question_vote(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote-down')
def decrease_question_vote(question_id):
    db_data_handler.decrease_question_vote(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up')
def increase_answer_vote(answer_id):
    answer = db_data_handler.increase_answer_vote(answer_id)
    return redirect('/question/' + str(answer['question_id']))


@app.route('/answer/<answer_id>/vote-down')
def decrease_answer_vote(answer_id):
    answer = db_data_handler.decrease_answer_vote(answer_id)
    return redirect('/question/' + str(answer['question_id']))


# ------------------- IMAGE ---------------------- #
def image_delete_from_server(item):
    if item['image'] != '':
        url_path = item['image']
        if url_path is not None:
            filename = url_path[len('/uploads/'):]
            filepath = UPLOAD_FOLDER + "/" + filename
            if os.path.exists(filepath):
                os.remove(filepath)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file):
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    count = len(fnmatch.filter(os.listdir('./sample_data/images'), '*.*'))
    new_name = "Ask-Mate-" + str(count) + os.urandom(4).hex() + "." + file_extension
    filename = secure_filename(new_name)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return 'NULL'
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return ''
        if file and allowed_file(file.filename):
            filename = save_image(file)
            return url_for('uploaded_file', filename=filename)


@app.route('/question/<question_id>/delete-image', methods=["GET"])
def edit_delete_image(question_id):
    question = db_data_handler.get_question(question_id)
    image_delete_from_server(question)
    question['image'] = ''
    db_data_handler.edit_question(question)
    return redirect('/question/' + question_id + '/edit')


# # ------------------- ERRORS ---------------------- #
# @app.route("/error")
# def display_error_message(error_id):
#     error_dict = {'id': error_id, "title": "Wrong file type!", "message": "Only .jpg and .png files accepted!"}
#     return error_dict


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
