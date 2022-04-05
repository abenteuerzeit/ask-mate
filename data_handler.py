import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_question_data():
    story = {}
    record = []
    result = []
    with open(DATA_FILE_PATH) as csvfile:
        for row in csvfile:
            if row.strip() == "id,submission_time,view_number,vote_number,title,message,image":
                continue
            else:
                record = row.split(',')
                for index, header in enumerate(DATA_HEADER):
                    story[header] = record[index]
                result.append(story)
    return result
