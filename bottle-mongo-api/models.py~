from mongoengine import Document, connect
from mongoengine import StringField, IntField

DB_NAME = 'eniso_fcee5'

class Student(Document):
    name = StringField(required=True)
    last_name = StringField(required=True)
    level = IntField(required=True, default=1)
    specialty = StringField(required=False, default="computer science")

connect(DB_NAME)
