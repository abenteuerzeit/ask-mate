from csv import DictWriter, DictReader
import os
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


def convert_to_datetime(epoch):
    return datetime.fromtimestamp(int(epoch))


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


def save_question_data(user_input):
    new_question = {'id': str(get_new_id(Q_FILE_PATH)), 'submission_time': NOW,
                    'view_number': '0', 'vote_number': '0', 'title': user_input['title'],
                    'message': user_input['message'], 'image': user_input['image']}
    with open(Q_FILE_PATH, 'a', newline=None) as csvfile:
        writer = DictWriter(csvfile, fieldnames=Q_HEADER)
        writer.writerow(new_question)
        csvfile.close()
    return new_question

def save_answer_data(user_input):
    new_answer = {'id': str(get_new_id(A_FILE_PATH)), 'submission_time': NOW, 'vote_number': '0',
                  'question_id': user_input['question_id'], 'message': user_input['message'],
                  'image': user_input['image']}
    with open(A_FILE_PATH, 'a', newline=None) as csvfile:
        writer = DictWriter(csvfile, fieldnames=A_HEADER)
        writer.writerow(new_answer)
        csvfile.close()
    return new_answer


def get_new_id(csvfile):
    with open(csvfile, 'r') as file:
        return int(max([q[0] for q in file.readlines() if q[0] != "i"])) + 1


if __name__ == '__main__':
    data = {}
    for i in Q_HEADER:
        data[i] = 'test'
    save_question_data(data)

"""
id,submission_time,view_number,vote_number,title,message,image
1,1493368154,29,7,"How to make lists in Python? I am totally new to this, any hints?",None
2,1493068124,15,9,"Wordpress loading multiple jQuery Versions.", "I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $('.myBook').booklet(); I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine. BUT in my theme i also using jquery via webpack so the loading order is now following: jquery booklet app.js (bundled file with webpack including jquery)","images/image1.png"
3,1493015432,1364,57,"Drawing canvas with an image picked with Cordova Camera Plugin., "I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS it throws errors such as cross origin issue or that I'm trying to use an unknown format. This is the code I'm using to draw the image (that works on web/desktop but not cordova built ios app)",None
"""
