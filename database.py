import peewee

db = peewee.MySQLDatabase('snake_sort', user='snake', passwd='password')


class match(peewee.Model):
    match_id = peewee.IntegerField()
    blue1 = peewee.CharField()
    blue2 = peewee.CharField()
    red1 = peewee.CharField()
    red2 = peewee.CharField()

    class Meta:
        database = db


def create_tables():
    match.create_table()
