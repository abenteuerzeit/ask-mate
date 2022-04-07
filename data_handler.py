import csv
import os

Q_FILE_PATH = os.getenv('Q_FILE_PATH') if 'Q_FILE_PATH' in os.environ else './sample_data/question.csv'
A_FILE_PATH = os.getenv('A_FILE_PATH') if 'A_FILE_PATH' in os.environ else './sample_data/answer.csv'
Q_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
A_HEADER = ['id','submission_time','vote_number','question_id','message','image']


def get_question_data():
    with open(Q_FILE_PATH) as csvfile:
        lines = [row.strip().split(",") for row in csvfile if Q_HEADER[0] not in row]
    return [{header: entry[index] for index, header in enumerate(Q_HEADER)} for entry in lines]


def get_answer_data():
    with open(A_FILE_PATH) as csvfile:
        lines = [row.strip().split(",") for row in csvfile if A_HEADER[3] not in row]
    return [{header: entry[index] for index, header in enumerate(A_HEADER)} for entry in lines]


if __name__ == '__main__':
    q = get_question_data()
    for line in q:
        print(line)

    a = get_answer_data()
    for line in a:
        print(line)
