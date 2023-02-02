from peewee import *


db = SqliteDatabase('report.db')


class MainModel(Model):
    id = PrimaryKeyField(null=False)

    class Meta:
        order_by = 'id'
        database = db

class Drivers(MainModel):

    code = CharField()
    name = CharField()

    class Meta:
        db_table = 'Drivers'


class Time(MainModel):

    code = ForeignKeyField(Drivers)
    start = DateTimeField()
    end = DateTimeField()

    class Meta:
        db_table = 'Time'
