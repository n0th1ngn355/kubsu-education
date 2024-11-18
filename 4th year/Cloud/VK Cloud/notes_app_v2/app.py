from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


db_service = 'http://localhost:5001/'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# # In-memory user storage (replace with a database in production)
# users = {'admin': User(id=1, username='admin', password='admin')}

def get_user(user):
    return User(user['id'], user['username'], user['password'])

@login_manager.user_loader
def load_user(user_id):
    response = requests.get(f'{db_service}user?id={user_id}')
    if response.status_code == 200:
        user = response.json()
        return get_user(user)
    return None

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = users.get(username)
#         if user and user.password == password:
#             login_user(user)
#             return redirect(url_for('index'))
#         flash('Invalid credentials', 'danger')
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Хэшируем пароль
        hashed_password = generate_password_hash(password)

        # Отправляем данные в базу
        response = requests.post(f'{db_service}users', json={
            'username': username,
            'password': hashed_password
        })

        if response.status_code == 201:
            login_user(get_user(response.json()))
            return redirect(url_for('login'))
        else:
            return 'User already exists or registration failed', 400

    return render_template('login.html', flag=1)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверяем данные
        response = requests.get(f'{db_service}users?username={username}')
        if response.status_code == 200:
            user = response.json()
            print(user)
            # print(check_password_hash(user['password'], password))
            if check_password_hash(user['password'], password):
                login_user(get_user(user))
                return redirect(url_for('index'))
            flash('Invalid credentials', 'danger')
    return render_template('login.html', flag=0)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    response = requests.get(f'{db_service}notes/{current_user.id}')
    notes = response.json() if response.status_code == 200 else []
    return render_template('index.html', notes=notes)

@app.route('/edit', methods=['GET'])
@app.route('/edit/<int:note_id>', methods=['GET'])
@login_required
def edit(note_id=None):
    note = None
    if note_id:
        response = requests.get(f'{db_service}note/{note_id}', json={'user_id': current_user.id})
        if response.status_code == 200:
            note = response.json()
            return render_template('edit.html', note=note)
        return redirect(url_for('edit'))
    return render_template('edit.html')


@app.route('/save', methods=['POST'])
@login_required
def save_note():
    data = request.json
    data['user_id']=current_user.id
    # print(data)
    if data['id']:  # Update existing note
        response = requests.put(f'{db_service}notes/{data["id"]}', json=data)
    else:  # Create new note
        response = requests.post(f'{db_service}notes', json=data)
    return jsonify({'success': response.status_code in [200, 201]})

# @app.route('/save', methods=['POST'])
# def save_note():
#     if 'user_id' not in session:
#         return jsonify({'error': 'Unauthorized'}), 401

#     data = request.json
#     data['user_id'] = session['user_id']

#     if 'id' in data:  # Update existing note
#         response = requests.put(f'{db_service}notes/{data["id"]}', json=data)
#     else:  # Create new note
#         response = requests.post('{db_service}notes', json=data)
#     return jsonify({'success': response.status_code in [200, 201]})


@app.route('/delete/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    response = requests.delete(f'{db_service}notes/{note_id}', json={'user_id': current_user.id})
    return jsonify({'success': response.status_code == 200})


if __name__ == '__main__':
    app.run(port=443, debug=False)
