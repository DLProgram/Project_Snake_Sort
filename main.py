#!/usr/bin/env python

import database
import os
from flask import Flask, render_template, session, request, redirect, url_for

SAVE_SESSION = True
app = Flask(__name__)


@app.before_request
def lock():
    if "/static" not in request.path and "/login" not in request.path:
        if 'username' not in session:
            return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = database.user.select().where(
            database.user.username == request.form['username'])
        if len(users) == 1:
            session['username'] = users[0].username
            session['role'] = users[0].role
        else:
            return render_template("login.html", error="Wrong credentials!")
        return redirect(url_for('index'))
    return render_template("login.html")

if __name__ == '__main__':
    if SAVE_SESSION:
        app.secret_key = os.urandom(24)
    else:
        app.secret_key = "+8\x0fUb\x84\xbe\xc1\xe6'@\x03\xb5\x08?oT.8?_\x88"
    app.run(host='0.0.0.0')
