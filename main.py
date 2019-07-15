from flask import Flask, request, render_template,redirect, session, flash
import os
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "get-it-done.db"))
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'uber!337'

db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    # owner_id in homework, but that is silly
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, user):
        self.name = name
        self.completed = False
        self.user = user

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks = db.relationship('Task', backref='user')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    
    allowed_routes = ['login', 'register']

    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:

            flash('Logged in')
            session['email'] = email

            return redirect('/ ') 

        if not user:

            flash('User does exist', 'error')

        if  user and user.password != password:

            flash('Password does not match user', 'error')   

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()

        if not existing_user and password == verify:

            db.session.add(User(email, password))
            db.session.commit()
            session['email'] = email

            return redirect('/')

        if existing_user:
            flash('Duplicate User', 'error')

        if not existing_user and password != verify:
            flash('Passwords do not match!', 'error')

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():

    user = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        # below should be user not user.id per homework instructions
        new_task = Task(task_name, user)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False, user=user).all()
    completed_tasks = Task.query.filter_by(completed=True, user=user).all()
    

    return render_template(
        'todos.html', 
        title='Get it Done!', 
        tasks=tasks,
        completed_tasks=completed_tasks,
        )

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')



if __name__ == '__main__':
    app.run()
