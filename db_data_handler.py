from datetime import datetime

import connection

NOW = datetime.fromtimestamp(int(datetime.now().timestamp()))


@connection.connection_handler
def get_questions(cursor):  # fetchall()
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY submission_time
        """
    cursor.execute(query)  # wykonaj czytanie po linii
    return cursor.fetchall()


@connection.connection_handler
def search(cursor, search_phrase):
    if search_phrase is not None:
        search_phrase = '%' + search_phrase + '%'
        query = """
        SELECT  question.id, title, question.message as question_message,
                answer.message as answer_message, 
                tag.name as tag
        FROM question
        LEFT JOIN answer
        ON question.id = answer.question_id
        LEFT JOIN question_tag qt on question.id = qt.question_id
        LEFT JOIN tag on qt.tag_id = tag.id
        WHERE  LOWER(title) LIKE LOWER(%(search_phrase)s)
            OR LOWER(question.message) like LOWER(%(search_phrase)s)
            OR LOWER(answer.message) LIKE LOWER(%(search_phrase)s)
            OR LOWER(tag.name) LIKE LOWER(%(search_phrase)s)
        """
        cursor.execute(query, {'search_phrase': search_phrase})
        return cursor.fetchall()


@connection.connection_handler
def get_question(cursor, id):  # fetchone()
    query = """
        SELECT *
        FROM question
        WHERE id = %s
    """
    cursor.execute(query, (id,))
    return cursor.fetchone()


@connection.connection_handler
def get_answers(cursor):
    query = """
        SELECT *
        from answer
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_for_question(cursor, question_id):
    query = """
        SELECT *
        from answer
        WHERE question_id =  %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_comments(cursor):
    return []


@connection.connection_handler
def get_comment_for_question(cursor, answer_id):
    return []


@connection.connection_handler
def get_comment_for_answer(cursor, answer_id):
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count
        FROM comment
        WHERE answer_id=%s
    """
    cursor.execute(query, (answer_id, ))
    return cursor.fetchall()


@connection.connection_handler
def delete_comment(cursor, id):
    query = """
        DELETE FROM comment
        WHERE id=%s
    """
    cursor.execute(query, (id,))


@connection.connection_handler
def delete_question_comment(cursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id=%s
    """
    cursor.execute(query, (question_id, ))


@connection.connection_handler
def increase_question_view_count(cursor, select_qdict):
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE question.id = %s
    """
    cursor.execute(query, (select_qdict,))


@connection.connection_handler
def increase_question_vote(cursor, selected_dictionary):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE question.id = %s
    """
    cursor.execute(query, (selected_dictionary,))


@connection.connection_handler
def increase_answer_vote(cursor, selected_dictionary):
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE answer.id = %s
        """
    cursor.execute(query, (selected_dictionary,))
    return get_question_id(cursor, selected_dictionary)


@connection.connection_handler
def decrease_question_vote(cursor, selected_dictionary):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE question.id = %s
    """
    cursor.execute(query, (selected_dictionary,))
    return get_question_id(cursor, selected_dictionary)


@connection.connection_handler
def decrease_answer_vote(cursor, selected_dictionary):
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE answer.id = %s
            """
    cursor.execute(query, (selected_dictionary,))
    return get_question_id(cursor, selected_dictionary)


def get_question_id(cursor, answer_id):
    query = """
            SELECT question_id
            from answer
            WHERE id = %s
            """
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


def set_image_to_null(table):
    if table == 'question':
        return """
                    UPDATE question
                    SET image = NULL
                    WHERE image = 'NULL' or image = '' or image = 'None'
                """
    elif table == 'answer':
        return """
                    UPDATE answer
                    SET image = NULL
                    WHERE image = 'NULL' or image = '' or image = 'None'
                """


@connection.connection_handler
def save_new_question_data(cursor, user_input):
    image = 'NULL' if user_input.get('image') == "" else user_input.get('image')
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES(%(time)s, 0, 0,  %(title)s, %(message)s, %(image)s)
            """
    cursor.execute(query, {'time': NOW,
                           'title': user_input.get('title'),
                           'message': user_input.get('message'),
                           'image': image})
    cursor.execute(set_image_to_null('question'))
    query = """
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
    question_id = int(updated_dict.get('id'))
    query = """
        UPDATE question
        SET title = %(title)s,
            message = %(message)s,
            image = %(image)s
        WHERE question.id = %(question_id)s
    """
    cursor.execute(query, {'title': updated_dict.get('title'),
                           'message': updated_dict.get('message'),
                           'image': updated_dict.get('image'),
                           'question_id': question_id})
    cursor.execute(set_image_to_null('question'))


@connection.connection_handler
def save_answer_data(cursor, user_input):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (%(time)s, 0, %(question_id)s, %(message)s, %(image)s)
    """
    cursor.execute(query, {'time': NOW, 'title': user_input.get('title'), 'question_id': user_input.get('question_id'),
                           'message': user_input.get('message'), 'image': user_input.get('image')})
    cursor.execute(set_image_to_null('answer'))
    query = """
            SELECT max(id) AS id
            from answer
        """
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def delete_question(cursor, id):
    query = """
    DELETE FROM question
    WHERE question.id = %s
    """
    cursor.execute(query, (id,))


@connection.connection_handler
def delete_answer(cursor, id):
    query = """
    DELETE FROM answer
    WHERE answer.id = %s
    """
    cursor.execute(query, (id,))


@connection.connection_handler
def get_question_tag_ids(cursor, question_id):
    query = """
    SELECT tag_id
    FROM question_tag
    WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_question_tags(cursor):
    query = """
    SELECT *
    FROM question_tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tags(cursor):
    query = """
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tag_id(cursor, name):
    query = """
    SELECT id
    FROM tag
    WHERE name = %s
    """
    cursor.execute(query, (name,))
    return cursor.fetchone()


@connection.connection_handler
def assign_tag_to_question(cursor, question_id, tag_id):
    query = """
    INSERT INTO question_tag (question_id, tag_id) 
    VALUES (%(question_id)s, %(tag_id)s)
    """
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def create_new_tag(cursor, name):
    query = """
    INSERT INTO tag (name)
    VALUES (%s)
    """
    cursor.execute(query, (name,))


@connection.connection_handler
def delete_tag_from_question(cursor, question_id, tag_id):
    query = """
    DELETE FROM question_tag
    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
    """
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def register_user(cursor, data):
    cursor.execute("""
    INSERT INTO users (username, passwordhash, submission_time)
    VALUES (%(username)s, %(password)s, %(date)s)
    """, data)


@connection.connection_handler
def users(cursor, username):
    cursor.execute("""
    SELECT passwordhash
    FROM users
    WHERE username=%s
    """, (username, ))
    return cursor.fetchone()