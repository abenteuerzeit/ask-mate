from datetime import datetime

import connection

NOW = datetime.fromtimestamp(int(datetime.now().timestamp()))


@connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT  id, submission_time, view_number, vote_number, title, message, image
        FROM    question
        ORDER BY submission_time
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search(cursor, search_phrase):
    if search_phrase is not None:
        search_phrase = '%' + search_phrase + '%'
        query = """
        SELECT  question.id, title, question.message as question_message,
                tag.name as tag
        FROM question
        LEFT JOIN question_tag qt on question.id = qt.question_id
        LEFT JOIN tag on qt.tag_id = tag.id
        WHERE  LOWER(title) LIKE LOWER(%(search_phrase)s)
            OR LOWER(question.message) LIKE LOWER(%(search_phrase)s)
            OR LOWER(tag.name) LIKE LOWER(%(search_phrase)s)
        """
        cursor.execute(query, {'search_phrase': search_phrase})
        return cursor.fetchall()


@connection.connection_handler
def search_answers(cursor, search_phrase):
    if search_phrase is not None:
        search_phrase = '%' + search_phrase + '%'
        query = """
        SELECT id as answer_id, question_id, message
        FROM answer
        WHERE LOWER(message) LIKE LOWER(%(search_phrase)s)
        """
        cursor.execute(query, {'search_phrase': search_phrase})
        return cursor.fetchall()


@connection.connection_handler
def get_question_data(cursor, question_id):  # fetchone()
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image, author_id
        FROM question
        WHERE id = %s
    """
    cursor.execute(query, (question_id,))
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
def get_answer_data(cursor, answer_id):
    query = """
        SELECT *
        from answer
        WHERE id = %s
    """
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


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
def get_comment_for_answer(cursor, answer_id):
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count, author
        FROM comment
        WHERE answer_id = %s
    """
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_comment_data(cursor, question_id):
    query = """
        SELECT c.id AS id, answer_id, c.message AS message, c.submission_time AS submission_time, edited_count, author
        FROM question
        LEFT JOIN answer a on question.id = a.question_id
        LEFT JOIN comment c on a.id = c.answer_id
        WHERE question.id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def add_comment_to_question(cursor, user_input):
    cursor.execute(
        """
        INSERT INTO comment (question_id, message, submission_time, edited_count, author)
        VALUES (%(question_id)s, %(message)s,%(submission_time)s, %(edited_count)s, %(author)s);
        """, user_input)


@connection.connection_handler
def add_comment_to_answer(cursor, user_input):
    cursor.execute("""
    INSERT INTO comment (answer_id, message, submission_time, edited_count, author)
    VALUES (%(answer_id)s, %(message)s,%(submission_time)s, %(edited_count)s, %(author)s)    
    """, user_input)


@connection.connection_handler
def get_comment_for_question(cursor, comment_id):
    cursor.execute("""
            SELECT comment.id AS id, comment.question_id, 
            comment.message, comment.submission_time, users.username AS author, comment.edited_count
            FROM comment
            LEFT JOIN users ON users.id = comment.author
            WHERE question_id=%s
        """, (comment_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_comment_for_answer(cursor, answer_id):
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count
        FROM comment
        WHERE answer_id=%s
    """
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()


@connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id=%s
    """
    cursor.execute(query, (comment_id,))


@connection.connection_handler
def delete_question_comment(cursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id=%s
    """
    cursor.execute(query, (question_id,))


@connection.connection_handler
def increase_question_view_count(cursor, select_qdict):
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE question.id = %s
    """
    cursor.execute(query, (select_qdict,))


@connection.connection_handler
def increase_question_vote(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE question.id = %s
    """
    cursor.execute(query, (question_id,))


@connection.connection_handler
def increase_answer_vote(cursor, answer_id):
    query = """
        UPDATE      answer AS a
        SET         vote_number = a.vote_number + 1
        FROM        answer
        INNER JOIN  question ON question.id = question_id
        WHERE       answer.id = %(answer_id)s;
        
        SELECT      question_id
        FROM        answer
        WHERE       %(answer_id)s = id;
        """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def decrease_question_vote(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE question.id = %s
    """
    cursor.execute(query, (question_id,))


@connection.connection_handler
def decrease_answer_vote(cursor, answer_id):
    query = """
        UPDATE      answer AS a
        SET         vote_number = a.vote_number - 1
        FROM        answer
        INNER JOIN  question ON question.id = question_id
        WHERE       answer.id = %(answer_id)s;
        
        SELECT      question_id
        FROM        answer
        WHERE       %(answer_id)s = id;
        """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_question_id(cursor, answer_id):
    query = """
            SELECT question_id
            from answer
            WHERE id = %s
            """
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()




# def set_image_to_null(table):
#     if table == 'question':
#         return """
#                     UPDATE question
#                     SET image = NULL
#                     WHERE image = 'NULL' or image = '' or image = 'None'
#                 """
#     elif table == 'answer':
#         return """
#                     UPDATE answer
#                     SET image = NULL
#                     WHERE image = 'NULL' or image = '' or image = 'None'
#                 """


@connection.connection_handler
def save_new_question_data(cursor, user_input):
    image = None if user_input.get('image') == "" else user_input.get('image')
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image, author_id)
            VALUES(%(time)s, 0, 0,  %(title)s, %(message)s, %(image)s, %(author_id)s)
            """
    cursor.execute(query, {'time': NOW,
                           'title': user_input.get('title'),
                           'message': user_input.get('message'),
                           'image': image,
                           'author_id': user_input.get('author_id')})

    # cursor.execute(set_image_to_null('question'))
    query = """
        SELECT max(id) AS id
        from question
    """
    cursor.execute(query)
    return cursor.fetchone()


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
    # cursor.execute(set_image_to_null('question'))


@connection.connection_handler
def save_answer_data(cursor, user_input):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, author_id)
        VALUES (%(time)s, 0, %(question_id)s, %(message)s, %(image)s, %(author_id)s)
    """
    cursor.execute(query, {'time': NOW, 'title': user_input.get('title'),
                           'question_id': user_input.get('question_id'),
                           'message': user_input.get('message'),
                           'image': user_input.get('image'),
                           'author_id': user_input.get('author_id')})
    # cursor.execute(set_image_to_null('answer'))
    query = """
            SELECT max(id) AS id
            from answer
        """
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
    DELETE FROM question
    WHERE question.id = %s
    """
    cursor.execute(query, (question_id,))


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
    DELETE FROM comment
    WHERE answer_id = %(answer_id)s;
    DELETE FROM answer
    WHERE answer.id = %(answer_id)s;
    """
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def get_question_tag_ids(cursor, question_id):
    query = """
    SELECT tag.id AS tag_id, name
    FROM question_tag
    LEFT JOIN tag ON question_tag.tag_id = tag.id
    WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_unassigned_tags(cursor, question_id):
    query = """
    SELECT DISTINCT id, name FROM tag
    LEFT JOIN question_tag qt on tag.id = qt.tag_id
    WHERE name NOT IN
        (SELECT name FROM question_tag
        LEFT JOIN tag ON question_tag.tag_id = tag.id
        WHERE question_id = %s);
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
def count_questions_with_tag(cursor):
    query = """
    SELECT id, name, COUNT(question_id) AS amount
    FROM question_tag
    LEFT JOIN tag on question_tag.tag_id = tag.id
    GROUP BY id, name
    ORDER BY amount DESC
    """
    cursor.execute(query,)
    return cursor.fetchall()


@connection.connection_handler
def filter_questions_by_tag(cursor, tag_id):
    query = """
    SELECT question_id AS id, submission_time, view_number, vote_number, title, message, image, author_id, 
    t.id AS tag_id, name AS tag_name
    FROM question
    INNER JOIN question_tag qt on question.id = qt.question_id
    INNER JOIN tag t on qt.tag_id = t.id
    WHERE tag_id = %s
    ORDER BY view_number DESC
    """
    cursor.execute(query, (tag_id,))
    return cursor.fetchall()


@connection.connection_handler
def register_user(cursor, data):
    cursor.execute("""
    INSERT INTO users (username, passwordhash, submission_time)
    VALUES (%(username)s, %(password)s, %(date)s)
    """, data)


@connection.connection_handler
def users(cursor, username):
    cursor.execute("""
    SELECT id, passwordhash
    FROM users
    WHERE username=%s
    """, (username, ))
    return cursor.fetchone()


@connection.connection_handler
def get_username(cursor, user_id):
    query = """
    SELECT username
    FROM users
    WHERE id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

  
@connection.connection_handler
def get_users_name_time(cursor):
    cursor.execute("""
    SELECT username, submission_time
    FROM users
    """)
    return cursor.fetchall()


@connection.connection_handler
def count_user_comment_and_answer(cursor):
    cursor.execute("""
    SELECT users.id, users.username, users.submission_time, 
    COUNT(comment.author) AS comment_num, 
    COUNT(answer.author_id) AS answer_num
    FROM users
    LEFT JOIN comment ON users.id = comment.author
    LEFT JOIN answer ON users.id = answer.author_id
    GROUP BY users.id, users.username, users.submission_time
    """)
    return cursor.fetchall()


@connection.connection_handler
def count_user_question(cursor):
    cursor.execute("""
    SELECT users.id, users.username, users.submission_time,  COUNT(question.author_id) AS question_num
    FROM users
    LEFT JOIN question ON users.id = question.author_id
    GROUP BY users.id, users.username, users.submission_time
    """)
    return cursor.fetchall()


@connection.connection_handler
def get_author_id(cursor, username):
    cursor.execute("""
    SELECT id
    FROM users
    WHERE username = %s
    """, (username,))
    return cursor.fetchone()
