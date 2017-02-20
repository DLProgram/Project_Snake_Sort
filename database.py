import peewee

db = peewee.MySQLDatabase('snake_sort', user='snake', passwd='password')


class match(peewee.Model):
    """Table storing all the match data.

    Args:
        match_id(int): Id of the match.
        blue1(char): Blue Team Name 1.
        blue2(char): Blue Team Name 2.
        red1(char): Red Team Name 1.
        red2(char): Red Team Name 2.
    """
    match_id = peewee.IntegerField()
    blue1 = peewee.CharField()
    blue2 = peewee.CharField()
    red1 = peewee.CharField()
    red2 = peewee.CharField()

    class Meta:
        database = db


class user(peewee.Model):
    """Table storing all users.

    Args:
        username(char): Username
        password(char): Password
        role(char): role of the user, eg. admin, red, blue
    """
    username = peewee.CharField()
    password = peewee.CharField()
    role = peewee.CharField()

    class Meta:
        database = db


class entry(peewee.Model):
    """Table storing all entries.

    Args:
        team_name(Char): Team name
        match_num(Int): Match number

        auto(Int): Auto score
        speed(Int): Speed of the robot
        capacity(Int): Capacity rating
        driver(Int): Driver's skill

        hang(Bool): High hang in 10s
        cube(Bool): Cube in the far zone
        blocking(Bool): Blocking ability
    """
    team_name = peewee.CharField()
    match_num = peewee.IntegerField()

    auto = peewee.IntegerField()
    speed = peewee.IntegerField()
    capacity = peewee.IntegerField()
    driver = peewee.IntegerField()

    hang = peewee.BooleanField()
    cube = peewee.BooleanField()
    blocking = peewee.BooleanField()

    class Meta:
        database = db


class team(peewee.Model):
    """Table storing all teams.

    Args:
        team_name(Char): Team name

        auto(Int): Auto percentage
        speed(Int): Speed percentage
        capacity(Int): Capacity percentage
        driver(Int): Driver's skill percentage

        hang(Bool): High hang percentage
        cube(Bool): Cube percentage
        blocking(Bool): Blocking percentage
    """
    team_name = peewee.CharField()

    auto = peewee.FloatField()
    speed = peewee.FloatField()
    capacity = peewee.FloatField()
    driver = peewee.FloatField()

    hang = peewee.FloatField()
    cube = peewee.FloatField()
    blocking = peewee.FloatField()

    class Meta:
        database = db


def create_tables():
    """Try to create all the tables, print error message if table exists
    """
    try:
        match.create_table()
    except:
        print("Table match already exists")
    try:
        user.create_table()
        user.create(username="admin", password="admin", role="admin")
        user.create(username="red1", password="red1", role="red1")
        user.create(username="red2", password="red2", role="red2")
        user.create(username="blue1", password="blue1", role="blue1")
        user.create(username="blue2", password="blue2", role="blue2")
    except:
        print("Table user already exists")
    try:
        entry.create_table()
    except:
        print("Table entry already exists")

    try:
        team.create_table()
    except:
        print("Table team already exists")

if __name__ == '__main__':
    create_tables()
