import os
from csv import DictWriter, DictReader
import csv
from datetime import datetime

Q_FILE_PATH = os.getenv('Q_FILE_PATH') if 'Q_FILE_PATH' in os.environ else './sample_data/question.csv'
A_FILE_PATH = os.getenv('A_FILE_PATH') if 'A_FILE_PATH' in os.environ else './sample_data/answer.csv'
Q_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
A_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
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
    if type(dictionary_data) is list:  # do we need it?
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


def increase_question_view_count(select_qdict):
    # I don't know why it tries to get /question/None... This should not be here.
    # 127.0.0.1 - - [21/Apr/2022 22:12:56] "POST /question/4/edit HTTP/1.1" 302 -
    # 127.0.0.1 - - [21/Apr/2022 22:12:56] "GET /question/4 HTTP/1.1" 200 -
    # 127.0.0.1 - - [21/Apr/2022 22:12:56] "GET /static/css/main.css HTTP/1.1" 304 -
    # 127.0.0.1 - - [21/Apr/2022 22:12:56] "GET /question/None HTTP/1.1" 200 -
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


def edit_question(updated_dict):
    question_list = get_questions()
    original_question = get_question(updated_dict['id'])
    for heading in Q_HEADER:
        if updated_dict.get(heading):
            original_question[heading] = updated_dict[heading]
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
        return int(max([q[0] for q in file.readlines() if q[0] != "i"])) + 1


def delete_question(id):
    lines = []
    with open(Q_FILE_PATH, 'r') as readfile:
        reader = csv.reader(readfile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == id:
                    lines.remove(row)
    with open(Q_FILE_PATH, 'w') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(lines)


# def save_image(url):
#     return url


if __name__ == '__main__':
    # data = {}
    # for i in Q_HEADER:
    #     data[i] = 'test'
    # save_new_question_data(data)
    question = increase_view_count('4')
    print(question)

"""
id,submission_time,view_number,vote_number,title,message,image
1,1493368154,29,7,"How to make lists in Python? I am totally new to this, any hints?",None
2,1493068124,15,9,"Wordpress loading multiple jQuery Versions.", "I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $('.myBook').booklet(); I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine. BUT in my theme i also using jquery via webpack so the loading order is now following: jquery booklet app.js (bundled file with webpack including jquery)","images/image1.png"
3,1493015432,1364,57,"Drawing canvas with an image picked with Cordova Camera Plugin., "I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS it throws errors such as cross origin issue or that I'm trying to use an unknown format. This is the code I'm using to draw the image (that works on web/desktop but not cordova built ios app)",None

"""
