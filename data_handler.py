import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else './sample_data/question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_question_data():
    questions = {}
    result = []
    with open(DATA_FILE_PATH) as csvfile:
        for row in csvfile:
            if row.strip() == "id,submission_time,view_number,vote_number,title,message,image":
                continue
            else:
                record = row.split(",")
                for index, header in enumerate(DATA_HEADER):
                    questions[header] = record[index]  # Changes all values in list to those defined in dictionary
                    result.append(questions)

                    # question_dict["id"] = record[0]
                    # question_dict["submission_time"] = record[1]
                    # question_dict["view_number"] = record[2]
                    # question_dict["vote_number"] = record[3]
                    # question_dict["title"] = record[4]
                    # question_dict["message"] = record[5]
                    # question_dict["image"] = record[6]
                    # result.append(question_dict)
    return result


if __name__ == '__main__':
    res = get_question_data()
    for line in res:
        print(line)

