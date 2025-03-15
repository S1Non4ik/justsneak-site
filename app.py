from flask import Flask, render_template, jsonify, send_from_directory
from psycopg2 import Error
import psycopg2

app = Flask(__name__, static_url_path='', static_folder='static')

def get_db_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="?%LupRRG}W1nW8ryAV",
            host="localhost",
            port="5432",
            database="user_counter"
        )
        return connection
        print('Подключенно')

    except (Exception, Error) as error:
        print("Ошибка при подключении к PostgreSQL:", error)
        return None



@app.route('/<path:path>')
def send_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/visit', methods=['POST'])
def visit():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Не удалось подключиться к базе данных'}), 500
    try:
        cur = connection.cursor()
        cur.execute("UPDATE user_count SET count = count + 1;")
        connection.commit()
        cur.close()
        return jsonify({'message': 'Пользователь учтен'})
    except (Exception, Error):
        return jsonify({'error': 'Не удалось обновить счетчик пользователей'}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)