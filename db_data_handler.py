from datetime import datetime

import connection

NOW = datetime.fromtimestamp(int(datetime.now().timestamp()))


@connection.connection_handler
def get_questions(cursor):  # fetchall()
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY submission_time"""
    cursor.execute(query)  # wykonaj czytanie po linii
    return cursor.fetchall()


@connection.connection_handler
def search(cursor, search_phrase):
    query = f"""
    SELECT question.id, title, question.message as question_message, answer.message as answer_message
    FROM question
    LEFT JOIN answer
    ON question.id = answer.question_id
    WHERE  
        lower(title) LIKE lower('%{search_phrase}%')
        OR lower(question.message) LIKE lower('%{search_phrase}%')
        OR lower(answer.message) LIKE lower('%{search_phrase}%')
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question(cursor, id):  # fetchone()
    query = f"""
        SELECT *
        FROM question
        WHERE id = {id}
    """
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def get_answers(cursor):
    query = f"""
        SELECT *
        from answer
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_for_question(cursor, question_id):
    query = f"""
        SELECT *
        from answer
        WHERE question_id = {question_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comments(cursor):
    return []


@connection.connection_handler
def get_comment_for_question(cursor, answer_id):
    return []


@connection.connection_handler
def increase_question_view_count(cursor, select_qdict):
    query = f"""
        UPDATE question
        SET view_number = view_number + 1
        WHERE question.id = {select_qdict}
    """
    cursor.execute(query)


@connection.connection_handler
def increase_question_vote(cursor, selected_dictionary):
    query = f"""
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE question.id = {selected_dictionary}
    """
    cursor.execute(query)


@connection.connection_handler
def increase_answer_vote(cursor, selected_dictionary):
    query = f"""
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE answer.id = {selected_dictionary}
        """
    cursor.execute(query)
    return get_question_id(cursor, selected_dictionary)


@connection.connection_handler
def decrease_question_vote(cursor, selected_dictionary):
    query = f"""
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE question.id = {selected_dictionary}
    """
    cursor.execute(query)
    return get_question_id(cursor, selected_dictionary)


@connection.connection_handler
def decrease_answer_vote(cursor, selected_dictionary):
    query = f"""
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE answer.id = {selected_dictionary}
            """
    cursor.execute(query)
    return get_question_id(cursor, selected_dictionary)


def get_question_id(cursor, answer_id):
    query = f"""
            SELECT question_id
            from answer
            WHERE id = {answer_id}
            """
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def save_new_question_data(cursor, user_input):
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES('{NOW}', 0, 0, '{user_input['title']}', '{user_input['message']}', 
        '{'NULL' if user_input['image'] == "" else user_input['image']}')
    """
    cursor.execute(query)
    query = f"""
        UPDATE question
        SET image = NULL
        WHERE image = 'NULL' or image = '' or image = 'None'
    """
    cursor.execute(query)
    query = f"""
        SELECT max(id) AS id
        from question
    """
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def save_new_comment(cursor, user_input):
    return []


@connection.connection_handler
def edit_question(cursor, updated_dict):
    query = f"""
        UPDATE question
        SET title = '{updated_dict['title']}',
            message = '{updated_dict['message']}',
            image = '{updated_dict['image']}'
        WHERE question.id = {updated_dict['id']}
    """
    cursor.execute(query)
    query = f"""
            UPDATE question
            SET image = NULL
            WHERE image = 'NULL' or image = '' or image = 'None'
        """
    cursor.execute(query)


@connection.connection_handler
def save_answer_data(cursor, user_input):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES ('{NOW}', 0, '{user_input['question_id']}', '{user_input['message']}', 
        '{user_input['image']}')
    """
    cursor.execute(query)
    query = f"""
            UPDATE answer
            SET image = NULL
            WHERE image = 'NULL' or image = '' or image = 'None'
        """
    cursor.execute(query)
    query = f"""
            SELECT max(id) AS id
            from answer
        """
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def delete_question(cursor, id):
    query = f"""
    DELETE FROM question
    WHERE question.id = {id}
    """
    cursor.execute(query)


@connection.connection_handler
def delete_answer(cursor, id):
    query = f"""
    DELETE FROM answer
    WHERE answer.id = {id}
    """
    cursor.execute(query)


@connection.connection_handler
def get_question_tag_ids(cursor, question_id):
    query = f"""
    SELECT tag_id
    FROM question_tag
    WHERE question_id = {question_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_tags(cursor):
    query = f"""
    SELECT *
    FROM question_tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tags(cursor):
    query = f"""
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def assign_tag_to_question(question_id, tag_id):
    query = f"""
    INSERT INTO question_tag (question_id, tag_id) 
    VALUES ({question_id}, {tag_id})
    """
    cursor.execute(query)


@connection.connection_handler
def create_new_tag(cursor, name):
    query = f"""
    INSERT INTO tag (name)
    VALUES ('{name}')
    """
    cursor.execute(query)
