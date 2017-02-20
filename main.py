#!/usr/bin/env python

import database
import os
import operator
from flask import Flask, render_template, session, request, redirect, url_for
from flask import abort
import vex_via_wrapper

SAVE_SESSION = True
app = Flask(__name__)

no_lock_pages = ["/static", "/login", "/logout"]
admin_lock_pages = ["/get_events", "/get_divisions",
                    "/get_matches", "/save_match_data",
                    "/manage_teams"]


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
        return redirect(url_for('manage_teams'))


@app.route('/scout/<int:match_num>', methods=['GET', 'POST'])
def scout(match_num):
    if request.method == 'POST':
        if process_request(match_num):
            return redirect(url_for('scout', match_num=match_num + 1))
    return render_template('scout.html',
                           team=get_team_num(match_num, session['role']),
                           match=match_num)


def get_team_num(match_num, color):
    if color == "red1":
        return database.match.get(database.match.match_id == match_num).red1
    elif color == "red2":
        return database.match.get(database.match.match_id == match_num).red2
    elif color == "blue1":
        return database.match.get(database.match.match_id == match_num).blue1
    elif color == "blue2":
        return database.match.get(database.match.match_id == match_num).blue2
    else:
        return "Admin"


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


@app.route("/get_events")
def get_events():
    data = []
    for e in vex_via_wrapper.get_events():
        data.append({'id': e[0], 'name': e[1], 'location': e[2]})
    return render_template("vex_via.html", type="event", data=data)


@app.route("/get_divisions/<event_id>")
def get_divisions(event_id):
    data = []
    for e in vex_via_wrapper.get_divisions(event_id):
        data.append({'id': e[0], 'name': e[1], 'event_id': event_id})
    return render_template("vex_via.html", type="division", data=data)


@app.route("/get_matches/<event_id>/<division_id>")
def get_matches(event_id, division_id):
    data = []
    for m in vex_via_wrapper.get_matches(event_id, division_id):
        if m[0] == '2':
            data.append({"id": m[2], "red1": m[5], "red2": m[
                        6], "blue1": m[8], "blue2": m[9]})
    return render_template("vex_via.html", type="match", data=data,
                           event_id=event_id, division_id=division_id)


@app.route("/save_match_data/<event_id>/<division_id>")
def save_match_data(event_id, division_id):
    for m in vex_via_wrapper.get_matches(event_id, division_id):
        if m[0] == '2':
            database.match.create(match_id=m[2],
                                  red1=m[5],
                                  red2=m[6],
                                  blue1=m[8],
                                  blue2=m[9])

    return render_template("dialog.html", type="suss", title="Success!",
                           text="Match data saved to database!")


@app.route("/manage_teams", methods=['GET', 'POST'])
def manage_teams():
    if request.method == 'POST':
        team_name = request.form["team_name"]

        auto = int(request.form["auto"])
        speed = int(request.form["speed"])
        capacity = int(request.form["capacity"])
        driver = int(request.form["driver"])

        hang = int(request.form["hang"])
        cube = int(request.form["cube"])
        blocking = int(request.form["blocking"])
        total = auto + speed + capacity + driver + hang + cube + blocking
        database.team.create(team_name=team_name,
                             auto=auto / total * 100,
                             speed=speed / total * 100,
                             capacity=capacity / total * 100,
                             driver=driver / total * 100,
                             hang=hang / total * 100,
                             cube=cube / total * 100,
                             blocking=blocking / total * 100)
    teams = []
    for team in database.team.select():
        teams.append({"team_name": team.team_name,
                      "auto": team.auto,
                      "speed": team.speed,
                      "capacity": team.capacity,
                      "driver": team.driver,
                      "hang": team.hang,
                      "cube": team.cube,
                      "blocking": team.blocking})
    return render_template("team.html", teams=teams)


@app.route("/team_picklist/<team_name>")
def team_picklist(team_name):
    team = database.team.get(database.team.team_name == team_name)
    picklist = generate_picklist(team)
    return render_template("picklist.html",
                           team_name=team_name, picklist=picklist)


def get_list_of_teams():
    teams = set()
    for team in database.entry.select():
        teams.add(team.team_name)
    return teams


def generate_picklist(team_preference):
    picklist = []
    for team in get_list_of_teams():
        match_scores = []
        for match in database.entry.select().where(database.entry.team_name == team):
            auto = match.auto * team_preference.auto / 100
            speed = match.speed * team_preference.speed / 100
            capacity = match.capacity * team_preference.capacity / 100
            driver = match.driver * team_preference.driver / 100

            hang = match.hang * team_preference.hang / 100
            cube = match.cube * team_preference.cube / 100
            blocking = match.blocking * team_preference.blocking / 100

            total = auto + speed + capacity + driver + hang + cube + blocking
            match_scores.append(total)
        match_scores.sort()
        if (len(match_scores) > 3):
            match_scores = match_scores[1:-1]
        picklist.append({"team_name": team, "score": sum(
            match_scores) / max(len(match_scores), 1)})
    picklist.sort(key=operator.itemgetter('score'), reverse=True)
    return picklist


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
