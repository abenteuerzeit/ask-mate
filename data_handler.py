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
    #         line[1] = datetime.datetime.fromtimestamp(int(line[1])).strftime('%Y-%m-%d %H:%M:%S')
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



def save_question_data():
    pass


def save_answer_data():
    pass


if __name__ == '__main__':
    q = get_answer_data()
    print(q)

    # a = get_answer_data()
    # for line in a:
    #     print(line)
