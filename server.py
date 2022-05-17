import bcrypt
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session
from datetime import datetime

import db_data_handler
import util
from bonus_questions import SAMPLE_QUESTIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = util.UPLOAD_FOLDER
app.config['SECRET_KEY'] = util.SECRET_KEY


@app.route('/list')
@app.route('/search')
@app.route('/')
def list_questions():
    order_by, order_direction = util.sort_questions()
    db_questions = db_data_handler.get_questions()
    db_questions.sort(key=lambda question: question[order_by], reverse=(order_direction == 'desc'))

    is_logged_in = False
    if 'username' in session:
        is_logged_in = True
    session['question_id'] = None
    return render_template('list.html', questions=db_questions,
                           order_by=order_by, order_direction=order_direction,
                           results=db_data_handler.search(request.args.get('q')),
                           answers=db_data_handler.search_answers(request.args.get('q')),
                           tags=db_data_handler.get_tags(), question_tags=db_data_handler.get_question_tags(),
                           is_logged_in=is_logged_in,
                           username=session.get('username'))


@app.route('/users')
def users():
    if 'username' not in session:
        flash('Please login to see the user list')
        return redirect(url_for('login'))
    if request.method == 'GET':
        comment_and_answer = db_data_handler.count_user_comment_and_answer()
        question = db_data_handler.count_user_question()
        return render_template('users.html', comment_and_answer=comment_and_answer, question=question)
    return redirect(url_for('list_questions'))


@app.route('/user/<user_id>')
def display_profile(user_id):
    if 'username' not in session:
        flash('Please login to see the user page')
        return redirect(url_for('list_questions'))
    comment_and_answer_count = db_data_handler.count_one_user_comment_and_answer(user_id)
    question_count = db_data_handler.count_one_user_question(user_id)
    return render_template('profile.html',
                           comment_and_answer=comment_and_answer_count,
                           question=question_count,
                           questions=db_data_handler.get_user_questions(user_id),
                           answers=db_data_handler.get_user_answers(user_id),
                           comments=db_data_handler.get_user_comments(user_id))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = bcrypt.hashpw((request.form.get('password')).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_data_handler.register_user({'username': username, 'password': password, 'date': db_data_handler.NOW})
        return redirect(url_for('list_questions'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        user_hash = db_data_handler.users(username)
        if user_hash is not None:
            if bcrypt.checkpw(password.encode('utf-8'), user_hash['passwordhash'].encode('utf-8')):
                session['user_id'], session['username'] = user_hash['id'], username
                if session['question_id'] is not None:
                    return redirect(url_for('display_question', question_id=session['question_id']))
                return redirect(url_for('list_questions'))
        flash('Bad login attempt. The username or password is invalid.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out')
    return redirect(url_for('list_questions'))


@app.route('/bonus-questions')
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route('/question/<question_id>')
def display_question(question_id):
    if request.method == 'GET':
        question = db_data_handler.get_question_data(question_id)
        db_data_handler.increase_question_view_count(question['id'])
        comments_question = db_data_handler.get_comment_for_question(question_id)
        session['question_id'] = question_id
        if request.args.get('change_answer_status'):
            if 'username' not in session:
                flash("You need to be logged in.")
            elif session['user_id'] == question.get("author_id"):
                db_data_handler.change_answer_acceptance_status(session['user_id'], request.args.get('answer_id'))
            else:
                flash("Only the question author can accept answers or withdrawal acceptance.")
        return render_template('question.html', question=question,
                               answers=db_data_handler.get_answer_for_question(question_id),
                               tags=db_data_handler.get_tags(),
                               question_tags=db_data_handler.get_question_tag_ids(question_id),
                               comments_question=comments_question,
                               comments_answer=db_data_handler.get_comment_data(question_id))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if 'username' not in session:
        flash('You must be logged in to add a new question!')
        return redirect(url_for('list_questions'))
    if request.method == 'GET':
        return render_template('add-question.html')
    if request.method == 'POST':
        author_id = session['user_id']
        new_question = db_data_handler.save_new_question_data({
            'title': request.form.get('title', default='not provided'),
            'message': request.form.get('message', default='not provided'),
            'image': util.upload_image(), 'author_id': author_id})
        return redirect(url_for('display_question', question_id=new_question.get('id')))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    util.image_delete_from_server(db_data_handler.get_question_data(question_id))
    tags = db_data_handler.get_question_tag_ids(question_id)
    if tags:
        for tag in tags:
            db_data_handler.delete_tag_from_question(question_id, tag.get('tag_id'))
    answers = db_data_handler.get_answer_for_question(question_id)
    if answers:
        for answer in answers:
            util.image_delete_from_server(answer)
            comments = db_data_handler.get_comment_for_answer(answer.get('id'))
            for comment in comments:
                db_data_handler.delete_comment(comment.get('id'))
            db_data_handler.delete_answer(answer.get('id'))
    db_data_handler.delete_question_comment(question_id)
    db_data_handler.delete_question(question_id)
    return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = db_data_handler.get_question_data(question_id)
    tag_ids, tags = db_data_handler.get_question_tag_ids(question_id), db_data_handler.get_tags()
    if request.method == 'GET':
        return render_template('edit-question.html', question=question, tag_ids=tag_ids, tags=tags)
    elif request.method == 'POST':
        if question['image'] is None:
            question['image'] = util.upload_image()
        db_data_handler.edit_question({'id': question_id,
                                       'title': request.form.get('title'),
                                       'message': request.form.get('message'),
                                       'image': question['image']})
        return redirect(url_for('display_question', question_id=question_id))


# ------------------- TAGS ---------------------- #
@app.route('/tags')
@app.route('/tags/<tag_id>')
def display_tags(tag_id=None):
    questions = db_data_handler.filter_questions_by_tag(tag_id)
    return render_template('tags.html', tags=db_data_handler.count_questions_with_tag(), questions=questions)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    question = db_data_handler.get_question_data(question_id)
    if request.method == 'GET':
        question_tags = db_data_handler.get_question_tag_ids(question_id)
        unassigned_tags = db_data_handler.get_unassigned_tags(question_id)
        return render_template('add-tag.html', question=question, tags=unassigned_tags, question_tags=question_tags)
    elif request.method == 'POST':
        name = request.form.get('add_tag')
        if util.already_exists(name):
            flash(f'"{name.capitalize()}" already exists! Only enter a name for a tag that does not exist.')
            flash('Choose a new tag by clicking on a button to assign the tag to the question.')
            return redirect(url_for('add_tag_to_question', question_id=question_id))
        tag_id = request.form.get('tag'),
        if name:
            db_data_handler.create_new_tag(name)
            tag_id = db_data_handler.get_tag_id(name)
            tag_id = tag_id.get('id')
        db_data_handler.assign_tag_to_question(question_id, tag_id)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag_from_question(question_id, tag_id):
    db_data_handler.delete_tag_from_question(question_id, tag_id)
    return redirect(url_for('display_question', question_id=question_id))


# ------------------- ANSWERS ---------------------- #
@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if 'username' not in session:
        flash('You must be logged in to add an answer!')
        return redirect(url_for('display_question', question_id=question_id))
    if request.method == 'GET':
        question = db_data_handler.get_question_data(question_id)
        answers = db_data_handler.get_answer_for_question(question_id)
        question['id'] = str(question.get('id'))
        return render_template('add-answer.html', question=question, answers=answers)
    elif request.method == 'POST':
        author_id = session['user_id']
        db_data_handler.save_answer_data({'message': request.form.get('message'), 'question_id': question_id,
                                          'image': util.upload_image(), 'author_id': author_id})
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = db_data_handler.get_answer_data(answer_id).get('question_id')
    util.image_delete_from_server(db_data_handler.get_answer_data(answer_id))
    db_data_handler.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


# ------------------- COMMENTS ---------------------- #
@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if 'username' not in session:
        flash('You must be logged in to comment a question')
        return redirect(url_for('display_question', question_id=question_id))
    if request.method == 'GET':
        return render_template('new-comment.html', question=db_data_handler.get_question_data(question_id))
    if request.method == 'POST':
        db_data_handler.add_comment_to_question(
            {'message': request.form.get('message'),
             'question_id': question_id,
             'submission_time': datetime.now(),
             'author': db_data_handler.get_author_id(session['username']).get("id"),
             'edited_count': 0})
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    question_id = db_data_handler.get_question_id(answer_id)
    if 'username' not in session:
        flash('You must be logged in to comment')
        return redirect(url_for('display_question', question_id=question_id.get('question_id')))
    if request.method == 'GET':
        return render_template('new-comment.html',
                               question=db_data_handler.get_question_data(question_id.get('question_id')))
    elif request.method == 'POST':
        db_data_handler.add_comment_to_answer(
            {'message': request.form.get('message'),
             'answer_id': answer_id,
             'submission_time': datetime.now(),
             'author': db_data_handler.get_author_id(session['username']).get('id'),
             'edited_count': 0})
        return redirect(url_for('display_question', question_id=question_id.get('question_id')))


# ------------------- VOTES ---------------------- #
@app.route('/question/<question_id>/vote-up')
def increase_question_vote(question_id):
    db_data_handler.increase_question_vote(question_id)
    return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/vote-down')
def decrease_question_vote(question_id):
    db_data_handler.decrease_question_vote(question_id)
    return redirect(url_for('list_questions'))


@app.route('/answer/<answer_id>/vote-up')
def increase_answer_vote(answer_id):
    answer = db_data_handler.increase_answer_vote(answer_id)
    return redirect(url_for('display_question', question_id=answer.get('question_id')))


@app.route('/answer/<answer_id>/vote-down')
def decrease_answer_vote(answer_id):
    answer = db_data_handler.decrease_answer_vote(answer_id)
    return redirect(url_for('display_question', question_id=answer.get('question_id')))


# ------------------- IMAGE ---------------------- #
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/question/<question_id>/delete-image')
def edit_delete_image(question_id):
    question = db_data_handler.get_question_data(question_id)
    util.image_delete_from_server(question)
    question['image'] = None
    db_data_handler.edit_question(question)
    return redirect('/question/' + question_id + '/edit')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
