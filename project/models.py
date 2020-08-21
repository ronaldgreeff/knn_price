import os
from datetime import datetime
from peewee import *
import json
import helpers

database = SqliteDatabase('database.db')

class BaseModel(Model):

    class Meta:
        database = database


class Site(BaseModel):
    netloc = CharField(null=False, unique=True)

class Page(BaseModel):
    site = ForeignKeyField(Site, backref='records',)# on_delete='CASCADE')
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



class DBReader():
    """ Manages reading from database """

    def con(self):
        return database
        # return query.sql()[0], database

    def q(self, query):
        """ executes sql query, fetches all """
        cursor = database.execute_sql(query)
        return cursor.fetchall()

class DBWriter():
    """ Manages writing to db including initial setup of tables """

    def __init__(self):
        """ build db """

        database.connect()
        with database:
            database.create_tables([Site, Page, Block, CSSKey, Computed])
        database.close()

    def store_page_extract(self, url, extract, purge_record=True):
        """ prepare extracted data then import it as part of a transaction
        which can be rollbacked in case of exception """

        parsed_url = helpers.urlparse(url)
        netloc = parsed_url[1]
        clean_url = helpers.unparse_url(parsed_url)

        valid_links = []
        for link in extract['links']:
            if helpers.link_in_netloc(netloc, link):
                valid_links.append(link)

        with database.atomic() as transaction:
            # to rollback if exception
            try:

                try:
                    site_obj = Site.create(netloc=netloc)
                except IntegrityError:
                    site_obj = Site.get(netloc=netloc)

                try:
                    page_obj = Page.get(url=clean_url)
                    if purge_record:
                        page_obj.delete_instance(recursive=True)
                        #todo: implement: raise Exception(Page.DoesNotExist)
                except Page.DoesNotExist:
                    page_obj = Page.create(
                        site=site_obj,
                        url=clean_url,
                        window_innerHeight=extract['env']['window_height'],
                        window_innerWidth=extract['env']['window_width'],
                        defaults=json.dumps(extract['env']['defaults'])
                        )

                for link in valid_links:
                    try:
                        Page.create(
                            site=site_obj,
                            url=link)
                    except IntegrityError:
                        pass

                for block in extract['texts']:

                    text = json.dumps(block['text']) # json.dumps([a list of texts])
                    bound = block['bound']

                    block_obj = Block.create(
                        page=page_obj,
                        text=text,
                        html=block['html'],
                        path=block['path'],
                        top=float(bound['top']),
                        left=float(bound['left']),
                        width=float(bound['width']),
                        height=float(bound['height']),
                    )
                    computed = block['computed']

                    for key, val in computed.items():

                        try:
                            key_obj = CSSKey.create(key=key)
                        except IntegrityError:
                            key_obj = CSSKey.get(key=key)

                        Computed.create(
                            block=block_obj,
                            key=key_obj,
                            val=val)

                page_obj.visited = True
                page_obj.save()

            except:
                transaction.rollback()
                raise
