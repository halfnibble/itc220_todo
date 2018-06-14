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
        SELECT id
        FROM identity
        WHERE user_id = %s
        AND passhprase = %s
        """
    cursor.execute(query, (user_id, passphrase))
    if len(cursor):
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

# @app.route('/create')
# def create_view():
#     return render_template('create.html')


# @app.route('/submit', methods=['POST'])
# def submit_view():
#     request.form['noun1']
#     return render_template('submit.html', context=context)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
