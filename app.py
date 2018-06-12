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
        SELECT id, name
        FROM todo;
        """
    cursor.execute(query)
    my_todos = []
    for id, name in cursor:
        my_todos.append({
            'id': id,
            'name': name
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
    # request.form['noun1']
    # return render_template('submit.html', context=context)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
