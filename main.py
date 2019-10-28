from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://builder:builder@localhost:3306/buildAblog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    post = db.Column(db.String(255))

    def __init__(self, title, post):
        self.title = title
        self.post = post

@app.route("/blog", methods=['GET', 'POST'])
def blogs():
    

@app.route("/newpost", methods=['GET', 'POST'])