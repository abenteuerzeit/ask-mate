import os
from csv import DictWriter, DictReader
from datetime import datetime

Q_FILE_PATH = os.getenv('Q_FILE_PATH') if 'Q_FILE_PATH' in os.environ else './sample_data/question.csv'
A_FILE_PATH = os.getenv('A_FILE_PATH') if 'A_FILE_PATH' in os.environ else './sample_data/answer.csv'
C_FILE_PATH = os.getenv('C_FILE_PATH') if 'C_FILE_PATH' in os.environ else './sample_data/comment.csv'
Q_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
A_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
C_HEADER = ['id', 'question_id', 'answer_id', 'message', 'submission_time', 'edited_count']
NOW = int(datetime.now().timestamp())


def get_questions():
    questions = []
    with open(Q_FILE_PATH) as csvfile:
        reader = DictReader(csvfile)
        for question in reader:
            question['submission_time'] = int(question['submission_time'])
            question['view_number'] = int(question['view_number'])
            question['vote_number'] = int(question['vote_number'])
            questions.append(question)
    return questions


def convert_to_datetime(dictionary_data):
    if type(dictionary_data) is list:
        for dictionary in dictionary_data:
            dictionary['submission_time'] = datetime.fromtimestamp(int(dictionary['submission_time']))
        return dictionary_data
    if type(dictionary_data) is dict:
        dictionary_data['submission_time'] = datetime.fromtimestamp(int(dictionary_data['submission_time']))
        return dictionary_data


def get_question(id):
    for question in get_questions():
        if question['id'] == id:
            return question
    return None


def get_answers():
    answers = []
    with open(A_FILE_PATH) as csvfile:
        reader = DictReader(csvfile)
        for answer in reader:
            answer['submission_time'] = int(answer['submission_time'])
            answer['vote_number'] = int(answer['vote_number'])
            answer['message'] = str(answer['message'])
            answers.append(answer)
    return answers


def get_answer_for_question(question_id):
    answers = []
    for answer in get_answers():
        if answer['question_id'] == question_id:
            answers.append(answer)
    return answers


def get_comments():
    comments = []
    with open(C_FILE_PATH) as csvfile:
        reader = DictReader(csvfile)
        for comment in reader:
            comment['submission_time'] = int(comment['submission_time'])
            comment['edited_count'] = int(comment['edited_count'])
            comment['message'] = str(comment['message'])
            comments.append(comment)
    return comments


def get_comment_for_question(answer_id):
    comments = []
    for comment in get_comments():
        if comment['answer_id'] == answer_id:
            comments.append(comment)
    return comments


def increase_question_view_count(select_qdict):
    # pass question id instead of the whole dictionary
    if select_qdict is not None:
        question_list = get_questions()
        for question_dictionary in question_list:
            if question_dictionary.get('id') == str(select_qdict['id']):
                question_dictionary['view_number'] = question_dictionary.get('view_number') + 1
                write_over(Q_FILE_PATH, Q_HEADER, question_list)


def increase_question_vote(selected_dictionary):
    question_list = get_questions()
    for q_dict in question_list:
        if q_dict.get('id') == str(selected_dictionary['id']):
            q_dict['vote_number'] = q_dict.get('vote_number') + 1
            write_over(Q_FILE_PATH, Q_HEADER, question_list)


def increase_answer_vote(selected_dictionary):
    answers = get_answers()
    for a_dict in answers:
        if a_dict.get('id') == str(selected_dictionary['id']):
            a_dict['vote_number'] = a_dict.get('vote_number') + 1
            write_over(A_FILE_PATH, A_HEADER, answers)


def decrease_question_vote(selected_dictionary):
    question_list = get_questions()
    for q_dict in question_list:
        if q_dict.get('id') == str(selected_dictionary['id']):
            q_dict['vote_number'] = q_dict.get('vote_number') - 1
            write_over(Q_FILE_PATH, Q_HEADER, question_list)


def decrease_answer_vote(selected_dictionary):
    answers = get_answers()
    for a_dict in answers:
        if a_dict.get('id') == str(selected_dictionary['id']):
            a_dict['vote_number'] = a_dict.get('vote_number') - 1
            write_over(A_FILE_PATH, A_HEADER, answers)


def save_new_question_data(user_input):
    question_list = get_questions()
    new_question = {'id': str(get_new_id(Q_FILE_PATH)), 'submission_time': NOW,
                    'view_number': '0', 'vote_number': '0', 'title': user_input['title'],
                    'message': user_input['message'], 'image': user_input['image']}
    question_list.append(new_question)
    write_over(Q_FILE_PATH, Q_HEADER, question_list)
    return new_question


def save_new_comment(user_input):
    comment_list = get_comments()
    new_comment = {'id': str(get_new_id(C_FILE_PATH)),
                   'question_id': str(get_new_id(Q_FILE_PATH)),
                   'answer_id': str(get_new_id(A_FILE_PATH)),
                   'message': user_input['message'],
                   'submission_time': NOW,
                   'edited_count': '0'}
    comment_list.append(new_comment)
    write_over(C_FILE_PATH, C_HEADER, comment_list)
    return new_comment


def edit_question(updated_dict):
    question_list = get_questions()
    original_question = get_question(updated_dict['id'])
    for heading in Q_HEADER:
        if updated_dict.get(heading):
            original_question[heading] = updated_dict[heading]
        if updated_dict['image'] is None:
            original_question['image'] = updated_dict['image']
    for index, q in enumerate(question_list):
        if q['id'] == updated_dict['id']:
            question_list[index] = original_question
    write_over(Q_FILE_PATH, Q_HEADER, question_list)


def save_answer_data(user_input):
    answer_list = get_answers()
    new_answer = {'id': str(get_new_id(A_FILE_PATH)), 'submission_time': NOW, 'vote_number': '0',
                  'question_id': user_input['question_id'], 'message': user_input['message'],
                  'image': user_input['image']}
    answer_list.append(new_answer)
    write_over(A_FILE_PATH, A_HEADER, answer_list)
    return new_answer


def write_over(file, header, content):
    with open(file, 'w', newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(content)


def get_new_id(csvfile):
    with open(csvfile, 'r') as file:
        return len(file.readlines())


def delete_question(id):
    question_list = get_questions()
    for index, question_dictionary in enumerate(question_list):
        if question_dictionary['id'] == id:
            del question_list[index]
    write_over(Q_FILE_PATH, Q_HEADER, question_list)


def delete_answer(id):
    answer_list = get_answers()
    for index, answer_dictionary in enumerate(answer_list):
        if answer_dictionary['id'] == id:
            del answer_list[index]
    write_over(A_FILE_PATH, A_HEADER, answer_list)
