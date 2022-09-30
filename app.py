from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import os

# Init app
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wqocylzqtgjgrh:bea150996387a0b1dc46b604764757244e5984c83931663a311576ea50edf299@ec2-3-219-135-162.compute-1.amazonaws.com:5432/dvraii2gtgvae'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)



# Task Class/Model
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description
        # self.user_id = user_id

# Task Schema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

# Init Schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Create a Task
@app.route('/task', methods=['POST'])
def add_task():
    title = request.json['title']
    description = request.json['description']
    # user_id = request.json['user_id']

    new_task = Task(title, description)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

# Get All Tasks
@app.route('/task', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Get Single Task
@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# Update a Task
@app.route('/task/<id>', methods=['PATCH'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']
    # user_id = request.json['user_id']

    task.title = title
    task.description = description
    # task.user_id = user_id

    db.session.commit()

    return task_schema.jsonify(task)

# Delete Task
@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)