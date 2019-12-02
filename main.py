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
    title = db.Column(db.String(30), unique=True)
    post = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=False)
    blogs = db.relationship('Blogs', backref='owner')

    def __init__(self, username, password, blogs):
        self.username = username
        self.password = password
        self.blogs = blogs   


@app.route("/", methods=['GET','POST'])
def index():
    blogs = None
    all_blogs = Blog.query.all()

    data_tuples = []

    user = None
    try:
        if session['logged_in']:
            blogs = Blog.query.filter(User.id == session["author_id"])
        else:
            pass
    except KeyError:
        pass

    for blog in all_blogs:
        author_object = User.query.get(blog.author_id)
        author_username = author_object.username
        object_tuple=(blog.name, blog.id, author_username)
        data_tuples.append(object_tuple)
    return render_template('blog.html', title="Blogz", blogs=blogs, user=user, data_tuples=data_tuples)


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
        user = User.query.filter(User.username == username).first()
        print(user)
        print(user.password)
        print(password)
        if user.password == password:
            session['logged_in'] = True
            session['author_id'] = user.id
            print(session)
            flash('Welcome')
            return render_template("blog.html", user=user)
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
        if not existing_user and not existing_username:
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
            new_entry = Blog(blog_title, blog_body)     
            db.session.add(new_entry)
            db.session.commit()        
            return redirect('/blog?id={}'.format(new_entry.id)) 
        else:
            return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error, 
                blog_title=blog_title, blog_body=blog_body)
    
    return render_template('newpost.html', title='New Entry')

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return render_template("blog.html")

@app.route("/blog/<blog_id>/", methods=['GET'])
def individual_entry(blog_id):
    blog = Blog.query.filter(blog_id).first()
    user = User.query.get(session['author_id'])

    return render_template("individual_entry.html",blog=blog, user=user)

if  __name__ == "__main__":
    app.run()
