from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# DB_USERNAME=os.getenv('DB_USERNAME')
# DB_PASSWORD=os.getenv('DB_PASSWORD')
# DB_HOST=os.getenv('DB_HOST')
# DB_NAME=os.getenv('DB_NAME')
# db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
# print(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Хранение хэша пароля
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)

@app.route('/note/<int:note_id>', methods=['GET'])
def get_note(note_id):
    data = request.json
    note = Note.query.filter_by(id=note_id, user_id=data['user_id']).first()
    if note:
        return jsonify({"id": note.id, "title": note.title, "content": note.content})
    return jsonify({"message": "Note not found"}), 404 

@app.route('/notes/<int:user_id>', methods=['GET'])
def get_notes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": n.id, "title": n.title, "content": n.content} for n in notes])

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.json
    note = Note(user_id=data['user_id'], title=data['title'], content=data['content'])
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note created"}), 201

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.json
    note = Note.query.filter_by(id=note_id, user_id=data['user_id']).first()
    if note:
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify({"message": "Note updated"})
    return jsonify({"message": "Note not found"}), 404


@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note_api(note_id):
    data = request.json
    note = Note.query.filter_by(id=note_id, user_id=data['user_id']).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Note not found or unauthorized'}), 404


# @app.route('/notes/<int:note_id>', methods=['DELETE'])
# def delete_note(note_id):
#     note = Note.query.get(note_id)
#     if note:
#         db.session.delete(note)
#         db.session.commit()
#         return jsonify({"message": "Note deleted"})
#     return jsonify({"message": "Note not found"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'password': new_user.password}), 201

@app.route('/users', methods=['GET'])
def get_user():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'password': user.password}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['GET'])
def get_user_by_id():
    user_id = request.args.get('id')
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'password': user.password}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=False)
