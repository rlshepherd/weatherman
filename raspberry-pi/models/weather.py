from peewee import *

database = SqliteDatabase('weather.db')

class BaseModel(Model):
    class Meta:
        database = database

class Weather(BaseModel):
    id = AutoField(unique = True, primary_key = True)
    datetime = DateTimeField()
    temperature = FloatField()
    humidity = FloatField()

