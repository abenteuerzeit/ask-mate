from datetime import datetime


def convert_to_datetime(dictionary_data):
    if type(dictionary_data) is list:
        for dictionary in dictionary_data:
            dictionary['submission_time'] = datetime.fromtimestamp(int(dictionary['submission_time']))
        return dictionary_data
    if type(dictionary_data) is dict:
        dictionary_data['submission_time'] = datetime.fromtimestamp(int(dictionary_data['submission_time']))
        return dictionary_data