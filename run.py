import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import os

#config

DATABASE = './golinks.db'
DEBUG = False # change to True if want debug features (and open remote code execution vulnerability so don't turn this on lightly!)
SECRET_KEY = 'SUPER_SECRET_KEY'
USERNAME = 'admin'
PASSWORD = 'SUPER_SECRET_PASSWORD'

#app
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/')
def home():
  cur = g.db.execute('select shorturl, longurl from urls order by id desc')
  urls = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
  return render_template('index.html', entries=urls)

@app.route('/<shorturl>')
def router(shorturl):
  cur = g.db.execute('select longurl from urls where shorturl = ?', [shorturl])
  url = ""
  for redirect_url in cur:
    url = redirect_url[0] #TODO better way to do this since it gets the last one (which should be fine)
  return redirect(url, code=302)
  #TODO http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/#configuring-apache

#POST ONLY
@app.route('/add', methods=['POST'])
def add_url():
  shorturl = request.form['shorturl']
  longurl = request.form['longurl']
  if(longurl[0:4] != 'http'):
    longurl = 'http://' + longurl #append http

  g.db.execute('insert into urls (longurl, shorturl) values (?, ?)', [longurl, shorturl])
  g.db.commit()
  flash('New Go/link made at go/{0}'.format(shorturl))
  return redirect(url_for('home'))

if __name__ == '__main__':
  if(not os.path.isfile(DATABASE)):
    init_db()
  app.run(host='0.0.0.0')
