from peewee import * 
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('after_thought.sqlite')

class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

class Category(BaseModel):
    name = CharField()
    author = ForeignKeyField(User, backref='categories')

class Thought(BaseModel):
    category = ForeignKeyField(Category, backref='category')
    body = CharField() 
    created_date = DateTimeField(default=datetime.datetime.now)
    starred = BooleanField(default=False)
    # author = ForeignKeyField(User, backref='thoughts')

class QuickThought(BaseModel):
    body = CharField()

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Category, Thought, QuickThought], safe=True)
    print('Connected to after_thought db, tables created!')
    DATABASE.close()