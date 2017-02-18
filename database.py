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


def create_tables():
    match.create_table()
    user.create_table()

if __name__ == '__main__':
    create_tables()
