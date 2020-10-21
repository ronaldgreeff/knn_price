from datetime import datetime
from peewee import *

database = SqliteDatabase(None)

class BaseModel(Model):

    class Meta:
        database = database

class Site(BaseModel):
    netloc = CharField(null=False, unique=True)

class Page(BaseModel):
    site = ForeignKeyField(Site, backref='records', on_delete='CASCADE')
    url = CharField(null=False, unique=True)
    visited = BooleanField(default=False)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())
    label = CharField(null=True)
    is_sale = BooleanField(null=True)
    window_innerHeight = IntegerField()
    window_innerWidth = IntegerField()
    defaults = CharField()

class Block(BaseModel):
    page = ForeignKeyField(Page, on_delete='CASCADE')
    text = CharField()
    html = CharField()
    label = CharField(null=True)
    path = CharField()
    width = DecimalField()
    height = DecimalField()
    left = DecimalField()
    top = DecimalField()

class CSSKey(BaseModel):
    key = CharField(unique=True)

class Computed(BaseModel):
    block = ForeignKeyField(Block, on_delete='CASCADE')
    key = ForeignKeyField(CSSKey)
    val = CharField(null=True)
