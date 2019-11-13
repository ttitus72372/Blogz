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
    post = db.Column(db.Text())

    def __init__(self, title, post):
        self.title = title
        self.post = post

@app.route("/blog", methods=['GET', 'POST'])
def blogs():
    post_id = request.args.get('id')
    title = "Build a Blog"

    if post_id:
        blog = Blog.query.filter_by(id = pots_id).all()
        return render_template('blog.html', title = title, blog = blog, post_id = post_id)
    else:
        blog = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('blog.html', title = title, blog = blog)

@app.route("/newpost", methods=['GET', 'POST'])
def create_new_post():
    blog_title = ""
    blog_content = ""
    title_error = ""
    content_error = ""

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        new_post = Blog[blog_title, blog_content]

        if blog_title == "":
            title_error = "Please enter a title!"

        if blog_content == "":
            content_error = "Please enter a post!"

        if title_error == "" and content_error == "":
            db.session.add(new_post)
            db.session.commit()

            return redirect('/?id={}'.format(new_post.id))

    return render_template('newpost.html', title = "Add a new post", blog_title = blog_title, blog_content = blog_content, title_error = title_error, content_error = content_error)

if __name__ == "__main__":
app.run()
