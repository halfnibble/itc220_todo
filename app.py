import os
from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
app = Flask(__name__)


connection = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME'),
)
cursor = connection.cursor()


def get_login_users():
    query = """
        SELECT u.id, u.first_name, u.last_name
        FROM user u LEFT JOIN identity i
        ON i.user_id = u.id
        WHERE i.id IS NOT NULL
        """
    cursor.execute(query)
    users = [{
        'id': id,
        'first_name': first_name,
        'last_name': last_name
    } for id, first_name, last_name in cursor]
    return users


def is_valid_login(user_id=None, passphrase=''):
    query = """
        SELECT COUNT(id)
        FROM identity
        WHERE user_id = %s
        AND passphrase = %s
        """
    cursor.execute(query, (user_id, passphrase))
    result = cursor.fetchone()
    if result[0] > 0:
        return True
    else:
        return False


def insert_todo(created_by=None, name=None, location=None):
    query = """
        INSERT INTO todo (created_by, name, location)
        VALUES (%s, %s, %s)
        """
    cursor.execute(query, (created_by, name, location))
    new_id = cursor.lastrowid
    if new_id:
        return True
    else:
        return False


@app.route('/')
def list_view():
    query = """
        SELECT t.id, t.name, t.location, u.first_name, u.last_name
        FROM todo t LEFT JOIN user u
        ON t.created_by = u.id;
        """
    cursor.execute(query)
    my_todos = []
    for id, name, location, first_name, last_name in cursor:
        my_todos.append({
            'id': id,
            'name': name,
            'location': location,
            'first_name': first_name,
            'last_name': last_name,
        })
    context = {
        'todos': my_todos
    }
    return render_template('list_view.html', context=context)


@app.route('/login')
def login_view():
    context = {
        'users': get_login_users()
    }
    return render_template('login.html', context=context)


@app.route('/post_login', methods=['POST'])
def post_login():
    user_id = request.form['user_id']
    passphrase = request.form['passphrase']
    if is_valid_login(user_id=user_id, passphrase=passphrase):
        context = {
            'user_id': user_id,
            'passphrase': passphrase,
        }
        return render_template('create.html', context=context)
    else:
        context = {
            'users': get_login_users(),
            'message': 'Bad credentials',
        }
        return render_template('login.html', context=context)


@app.route('/post_create', methods=['POST'])
def post_create():
    user_id = request.form['user_id']
    passphrase = request.form['passphrase']
    name = request.form['name']
    location = request.form['location']
    if is_valid_login(user_id=user_id, passphrase=passphrase):
        result = insert_todo(
            created_by=user_id,
            name=name,
            location=location,
        )
        context = {
            'user_id': user_id,
            'passphrase': passphrase,
            'message': 'One New ToDo Created! Debug: {0}.'.format(result)
        }
        return render_template('create.html', context=context)
    else:
        context = {
            'users': get_login_users(),
            'message': 'Bad credentials',
        }
        return render_template('login.html', context=context)

    return render_template('create.html', context=context)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
