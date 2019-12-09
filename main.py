from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:@localhost:3306/Blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=False)
    post = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner_id):
        self.title = title
        self.post = post
        self.owner_id = owner_id
        

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=False)
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password   


@app.route("/", methods=['GET','POST'])
def index():
    error = None
    if session['logged_in']:
        if request.method == 'POST':
            blog_name = request.form['blog']
            new_blog = Blog(blog_name)
            db.session.add(new_blog)
            db.session.commit()
            blogs = Blog.query.filter_by(completed=False).all()
            completed_blogs = Blog.query.filter_by(completed=True).all()
            return render_template('blog.html', title="Blogz",blogs=blogs,completed_blogs=completed_blogs)
    return render_template('login.html', error=error)
    

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts, title='Build-a-blog')
    else:
        post = Blog.query.get(blog_id)
        body = Blog.query.get(blog_id)
        return render_template('post.html', post=post, body=body, title='Blog Entry')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['logged_in'] = True
            session['user'] = user.username
            session['user_id'] = user.id
            
            flash('Welcome')
            blogs = User.query.filter_by(username = session['user']).all()
            return render_template("blog.html", blogs=blogs, user=user)
        else:
            flash("Error: Try again because you do not have login or account.")
            return render_template('login.html', error=error)

    return render_template('login.html', error=error)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    password_error = None
    username_error = None

    if request.method == 'POST':
        print(type(request.form))
        password = request.form['password']
        verify = request.form['verify']
        username = request.form['username']
        existing_username = User.query.filter_by(username=username).first()
        print(existing_username)
        if not existing_username:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            print(new_user)
            return redirect('/login')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html', password_error=password_error, username_error=username_error)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title_error = ''
    body_error = ''
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        title_error = ''
        body_error = ''

        if not blog_title:
            title_error = "Please enter a blog title"
        if not blog_body:
            body_error = "Please enter a blog entry"

        if not body_error and not title_error:
            blog_title = request.form['blog-title']
            blog_body = request.form['blog-entry']
            owner_id = session['user_id']
            new_entry = Blog(blog_title, blog_body, owner_id)     
            db.session.add(new_entry)
            db.session.commit()  

            newentry_id = new_entry.id

            blogs = Blog.query.filter(User.username == session['user'])
            user = User.query.get(session['user'])     
            return render_template('blog.html', blogs=blogs, user=user) 
        else:
            return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error, 
                blog_title=blog_title, blog_body=blog_body)
    else:
        return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error)

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('logged_in', None)
    del session['user']
    del session['user_id']
    return render_template("blog.html")

@app.route("/blog/<blog_id>/", methods=['GET'])
def individual_entry(blog_id):
    blog = Blog.query.filter(blog_id).first()
    user = User.query.get(session['user'])

    return render_template("individual_entry.html",blog=blog, user=user)

app.secret_key='S3CR37K3Y1S5ECR3T'

if  __name__ == "__main__":
    app.run()
