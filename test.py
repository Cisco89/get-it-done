from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too

project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "test.db"))
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500))

    def __init__(self, task):
        self.task = task

# app.run()