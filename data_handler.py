import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else './sample_data/question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_question_data():
    with open(DATA_FILE_PATH) as csvfile:
        lines = [row.strip().split(",") for row in csvfile if DATA_HEADER[0] not in row]
    return [{header: entry[index] for index, header in enumerate(DATA_HEADER)} for entry in lines]


if __name__ == '__main__':
    res = get_question_data()
    for line in res:
        print(line)
