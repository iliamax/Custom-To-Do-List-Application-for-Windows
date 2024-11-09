from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from plyer import notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    due_date = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

# Function to initialize the database
def create_tables():
    db.create_all()

# Initialize the database when the app starts
with app.app_context():
    create_tables()

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    priority = data.get('priority')

    # Create a new task and add it to the database
    new_task = Task(title=title, description=description, due_date=due_date, priority=priority)
    db.session.add(new_task)
    db.session.commit()

    # Trigger a push notification if due date is near
    if datetime.strptime(due_date, "%Y-%m-%dT%H:%M") <= datetime.now():
        notification.notify(
            title='Task Reminder',
            message=f'Your task "{title}" is due soon!',
            timeout=10
        )

    return jsonify({'message': 'Task added successfully'}), 201

# Route to retrieve all tasks
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority
    } for task in tasks]
    return jsonify(task_list)

if __name__ == '__main__':
    app.run(debug=True)
