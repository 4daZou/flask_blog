import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

# flash() stores messages in the session, which needs a secret key
app.config["SECRET_KEY"] = "your secret key"


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')

    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn


# Function to get a single post by its id, or show a 404 page if it doesn't exist
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    # open a connection to the database
    conn = get_db_connection()

    # get all posts from the posts table, newest first
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()

    # close the connection
    conn.close()

    # send the posts to the index.html template to be displayed
    return render_template('index.html', posts=posts)


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    # the form was submitted
    if request.method == 'POST':
        # get the title and content the user entered
        title = request.form['title']
        content = request.form['content']

        # make sure both fields were filled in
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            # insert the new post into the database
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()

            # send the user back to the index page
            return redirect(url_for('index'))

    # a GET request (or a form with errors) shows the create form
    return render_template('create.html')


# route to edit a post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    # get the post being edited (404 if it doesn't exist)
    post = get_post(id)

    # the edit form was submitted
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            # update the post in the database
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    # show the edit form filled in with the post's current values
    return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run()
