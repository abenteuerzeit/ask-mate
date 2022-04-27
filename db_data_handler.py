import connection

@connection.connection_handler
def get_questions(cursor):  #fetchall()
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY submission_time"""
    cursor.execute(query)  #wykonaj czytanie po linii
    return cursor.fetchall()


@connection.connection_handler
def get_question(cursor, id):  #fetchone()
    return []


@connection.connection_handler
def get_answers(cursor):
    return []


@connection.connection_handler
def get_answer_for_question(cursor, question_id):
    return []


@connection.connection_handler
def get_comments(cursor):
    return []


@connection.connection_handler
def get_comment_for_question(cursor, answer_id):
    return []


@connection.connection_handler
def increase_question_view_count(cursor, select_qdict):
    return []


@connection.connection_handler
def increase_question_vote(cursor, selected_dictionary):
    return []


@connection.connection_handler
def increase_answer_vote(cursor, selected_dictionary):
    return []


@connection.connection_handler
def decrease_question_vote(cursor, selected_dictionary):
    return []


@connection.connection_handler
def decrease_answer_vote(cursor, selected_dictionary):
    return []


@connection.connection_handler
def save_new_question_data(cursor, user_input):
    return []


@connection.connection_handler
def save_new_comment(cursor, user_input):
    return []


@connection.connection_handler
def edit_question(cursor, updated_dict):
    return []


@connection.connection_handler
def save_answer_data(cursor, user_input):
    return []


@connection.connection_handler
def write_over(cursor, file, header, content):
    return []


@connection.connection_handler
def get_new_id(cursor, csvfile):
    return []


@connection.connection_handler
def delete_question(cursor, id):
    return []


@connection.connection_handler
def delete_answer(cursor, id):
    return []
