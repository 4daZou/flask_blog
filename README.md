# Flask Blog

A simple blogging application built with Python Flask and SQLite. Users can create, view, edit, and delete blog posts.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py             # creates database.db with sample posts
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Features

- **View posts** – the home page lists all posts, newest first
- **Create posts** – "New Post" in the nav bar
- **Edit posts** – "Edit" link under each post
- **Delete posts** – "Delete Post" button on the edit page

## Project structure

```
app.py            Flask application and routes
init_db.py        Creates the database and inserts sample posts
schema.sql        Table definition for posts
templates/        Jinja2 templates (base, index, create, edit)
```
