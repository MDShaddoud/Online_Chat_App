from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mahmoud@123'
app.config['MYSQL_DB'] = 'online_chat'
socketio = SocketIO(app)
mysql = MySQL(app)
api = Api(app)

# Create a table to store messages in MySQL
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(255), "
                "content TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE "
                "NOT NULL, password VARCHAR(255) NOT NULL)")
    mysql.connection.commit()
    cur.close()


# RESTful API
class MessagesResource(Resource):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM messages")
        messages = cur.fetchall()
        cur.close()
        return {'messages': messages}

    def post(self):
        data = request.get_json()
        user = data['user']
        content = data['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (user, content) VALUES (%s, %s)", (user, content))
        mysql.connection.commit()
        cur.close()
        emit('message', {'user': user, 'content': content}, broadcast=True)
        return {'message': 'Message posted successfully'}


api.add_resource(MessagesResource, '/messages')


# Route for signing up
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        session['username'] = request.form['username']
        return render_template('index.html', username=session['username'])
    return render_template('login.html')


@app.route('/app')
def index():
    return render_template('index.html')


# WebSocket
@socketio.on('user_join')
def handle_user_join(username):
    session['username'] = username
    emit('chat', {'username': 'System', 'message': f'{username} joined the chat'}, broadcast=True)


@socketio.on('new_message')
def handle_new_message(message):
    emit('chat', {'username': session['username'], 'message': message}, broadcast=True)


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
