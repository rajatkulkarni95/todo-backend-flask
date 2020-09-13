from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init Database
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# CORS
CORS(app)


# Todo Class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    isCompleted = db.Column(db.Boolean)

    def __init__(self, text, isCompleted):
        self.text = text
        self.isCompleted = isCompleted


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text', 'isCompleted')


# Init schema
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route('/todos', methods=['GET'])
def fetch_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)

    res = make_response(jsonify(result), 200)
    return res


@app.route('/todos', methods=['POST'])
def create_todo():
    text = request.json['text']
    isCompleted = request.json['isCompleted']

    new_todo = Todo(text, isCompleted)

    db.session.add(new_todo)
    db.session.commit()

    res = make_response(todo_schema.jsonify(new_todo), 200)
    return res


@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)

    isCompleted = request.json['isCompleted']

    todo.isCompleted = isCompleted

    db.session.commit()
    res = make_response(todo_schema.jsonify(todo), 200)
    return res


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()

    res = make_response(todo_schema.jsonify(todo), 200)
    return res


if __name__ == "__main__":
    app.run(debug=True)
