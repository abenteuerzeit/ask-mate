import ast
import fnmatch
import os

from flask import request, flash, url_for
from werkzeug.utils import secure_filename

import server
from db_data_handler import get_tags

ALLOWED_EXTENSIONS = {'jpg', 'png'}
UPLOAD_FOLDER = './static/images'
SECRET_KEY = os.urandom(12).hex()


def get_sorting_values():
    order_str = request.args.get('order_dict')
    if order_str:
        order_dict = ast.literal_eval(order_str)
        return order_dict.get('order_by'), order_dict.get('order_direction'),
    return request.args.get('order_dict', default='id'), request.args.get('order_direction', default='desc')


def image_delete_from_server(item):
    if item['image'] is not None:
        url_path = item['image']
        if url_path is not None:
            filename = url_path[len('/uploads/'):]
            filepath = UPLOAD_FOLDER + '/' + filename
            if os.path.exists(filepath):
                os.remove(filepath)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('File missing from request query')
            return None
        file = request.files['file']
        if file.filename == '':
            return None
        if file and allowed_file(file.filename):
            filename = save_image(file)
            return url_for('uploaded_file', filename=filename)
        else:
            flash('Only .jpg and .png files accepted!')
            return None


def save_image(file):
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    count = len(fnmatch.filter(os.listdir(UPLOAD_FOLDER), '*.*'))
    new_name = 'Ask-Mate-' + str(count) + os.urandom(4).hex() + '.' + file_extension
    filename = secure_filename(new_name)
    file.save(os.path.join(server.app.config['UPLOAD_FOLDER'], filename))
    return filename


def already_exists(tag):
    for tag_dict in get_tags():
        if tag == tag_dict.get('name'):
            return True
    return False
