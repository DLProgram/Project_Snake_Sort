#!/usr/bin/env python

import database
import os
from flask import Flask, render_template, session, request, redirect, url_for
from flask import abort

SAVE_SESSION = True
app = Flask(__name__)

no_lock_pages = ["/static", "/login", "/logout"]
admin_lock_pages = []


@app.before_request
def lock():
    for page in no_lock_pages:
        if page in request.path:
            return
    if 'username' not in session:
        return redirect(url_for('login'))
    for page in admin_lock_pages:
        if page in request.path:
            if session['role'] != "admin":
                abort(403)


@app.route('/', methods=['GET', 'POST'])
def index():
    if "red" in session['role'] or "blue" in session['role']:
        return redirect(url_for('scout', match_num=1))
    elif "admin" in session['role']:
        return redirect(url_for('admin'))


@app.route('/scout/<int:match_num>', methods=['GET', 'POST'])
def scout(match_num):
    if request.method == 'POST':
        if process_request(match_num):
            return redirect(url_for('scout', match_num=match_num + 1))
        else:
            return render_template('index.html', team="211Z", match=match_num)
    return render_template('index.html', team="211Z", match=match_num)


def process_request(match_num):
    team_name = request.form['team_name']

    auto = int(request.form['auto']) * 10
    speed = request.form['speed']
    capacity = request.form['capacity']
    driver = request.form['driver']

    hang = "hang" in request.form
    cube = "cube" in request.form
    blocking = "blocking" in request.form
    try:
        database.entry.create(team_name=team_name,
                              match_num=match_num,
                              auto=auto,
                              speed=speed,
                              capacity=capacity,
                              driver=driver,
                              hang=hang,
                              cube=cube,
                              blocking=blocking)
        return True
    except:
        return False


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = database.user.select().where(
            database.user.username == request.form['username'],
            database.user.password == request.form['password'])
        if len(users) == 1:
            session['username'] = users[0].username
            session['role'] = users[0].role
        else:
            return render_template("login.html", error="Wrong credentials!")
        return redirect(url_for('index'))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if SAVE_SESSION:
        app.secret_key = "+8\x0fUb\x84\xbe\xc1\xe6'@\x03\xb5\x08?oT.8?_\x88"
    else:
        app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0')
