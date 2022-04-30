from datetime import datetime
from csv import DictWriter, DictReader


def convert_to_datetime(dictionary_data):
    if type(dictionary_data) is list:
        for dictionary in dictionary_data:
            dictionary['submission_time'] = datetime.fromtimestamp(int(dictionary['submission_time']))
        return dictionary_data
    if type(dictionary_data) is dict:
        dictionary_data['submission_time'] = datetime.fromtimestamp(int(dictionary_data['submission_time']))
        return dictionary_data


def write_over(file, header, content):
    with open(file, 'w', newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(content)


def get_new_id(csvfile):
    with open(csvfile, 'r') as file:
        return len(file.readlines())
