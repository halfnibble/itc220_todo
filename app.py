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
