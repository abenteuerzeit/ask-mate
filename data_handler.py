import csv
import os
from datetime import datetime

Q_FILE_PATH = os.getenv('Q_FILE_PATH') if 'Q_FILE_PATH' in os.environ else './sample_data/question.csv'
A_FILE_PATH = os.getenv('A_FILE_PATH') if 'A_FILE_PATH' in os.environ else './sample_data/answer.csv'
Q_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
A_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_questions():
    # with open(Q_FILE_PATH) as csvfile:
    #     lines = [row.strip().split(",") for row in csvfile if Q_HEADER[0] not in row]
    #     for line in lines:
    #         line[1] = datetime.fromtimestamp(int(line[1])).strftime('%Y-%m-%d %H:%M:%S')
    # return sorted([{header: entry[index] for index, header in enumerate(Q_HEADER)}
    #                for entry in lines], key=lambda d: d['submission_time'], reverse=True)
    questions = []
    with open(Q_FILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for question in reader:
            question['submission_time'] = datetime.fromtimestamp(int(question['submission_time']))
            question['view_number'] = int(question['view_number'])
            question['vote_number'] = int(question['vote_number'])
            questions.append(question)
    return questions


def get_question(id):
    for question in get_questions():
        if question['id'] == id:
            return question
    return None


def get_answers():
    with open(A_FILE_PATH) as csvfile:
        lines = [row.strip().split(",") for row in csvfile if A_HEADER[3] not in row]
    return [{header: entry[index] for index, header in enumerate(A_HEADER)} for entry in lines]


def get_answer_for_question(question_id):
    answers = []
    for answer in get_answers():
        if answer['question_id'] == question_id:
            answers.append(answer)
    return answers


def save_question_data(user_input):
    question_list = get_questions()
    question_list.append({'id': str(get_new_id()), 'submission_time': int(datetime.now().timestamp()),
                          'view_number': '0', 'vote_number': '0', 'title': user_input["title"],
                          'message': user_input["message"], 'image': user_input['image']})
    with open(Q_FILE_PATH, 'w', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=Q_HEADER)
        writer.writeheader()
        writer.writerows(question_list)


def save_answer_data():
    pass


def get_new_id():
    with open(Q_FILE_PATH, 'r') as file:
        return int(max([q[0] for q in file.readlines() if q[0] != "i"])) + 1


if __name__ == '__main__':
    data = {}
    for i in Q_HEADER:
        data[i] = 'test'
    save_question_data(data)
    # q = get_answer_data()
    # print(q)


    # a = get_answer_data()
    # for line in a:
    #     print(line)


"""
id,submission_time,view_number,vote_number,title,message,image
1,1493368154,29,7,"How to make lists in Python? I am totally new to this, any hints?",None
2,1493068124,15,9,"Wordpress loading multiple jQuery Versions.", "I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $('.myBook').booklet(); I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine. BUT in my theme i also using jquery via webpack so the loading order is now following: jquery booklet app.js (bundled file with webpack including jquery)","images/image1.png"
3,1493015432,1364,57,"Drawing canvas with an image picked with Cordova Camera Plugin., "I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS it throws errors such as cross origin issue or that I'm trying to use an unknown format. This is the code I'm using to draw the image (that works on web/desktop but not cordova built ios app)",None
"""