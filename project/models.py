import os
from datetime import datetime
from peewee import *


database = SqliteDatabase('database.db')

class BaseModel(Model):

    class Meta:
        database = database


class Site(BaseModel):
    netloc = CharField(null=False, unique=True)

class Page(BaseModel):
    site = ForeignKeyField(Site, backref='records')
    label = CharField(null=True)
    page_title = CharField(unique=True)
    url = CharField(unique=True, null=False)
    visited = BooleanField(default=False)
    is_sale = BooleanField(null=True)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())

class Block(BaseModel):
    page = ForeignKeyField(Page, on_delete='CASCADE')
    label = CharField(null=True)
    text = CharField(max_length=64)
    html = CharField(max_length=64)
    width = DecimalField()
    height = DecimalField()
    left = DecimalField()
    top = DecimalField()

class CSSKey(BaseModel):
    key = CharField(unique=True)

class Computed(BaseModel):
    page = ForeignKeyField(Page, on_delete='CASCADE')
    key = ForeignKeyField(CSSKey)
    val = CharField(null=True)


class DBWriter():
    
    def __init__(self):

        database.connect()
        with database:
            database.create_tables([Site, Page, Block, CSSKey, Computed])
        database.close()

    def get_local_pages(self):
        """ Get folder (vendor) and file (html) list for pages in /data
            in the format {vendor: [page, ...], ...} """

        d = {}
        for vendor in os.listdir('data'):
            d[vendor] = ([file for file in os.listdir('data/{}'.format(vendor))
                if file[-4:] == 'html'])

        return d

    def get_local_page_paths(self):

        l = []
        d = self.get_local_pages()
        for vendor in d:
            for file in d[vendor]:
                l.append( os.path.join(os.getcwd(), 'data', vendor, file) )

        return l

    def store_extract(self, url=None, extract):

        if url:
            parsed_url = urlparse(url)

        cleaned_links = []
        for link in extract['links']:
            parsed_link = urlparse(link)
            if parsed_link[1] == parsed_url[1]:
                cleaned_links.append(urlunparse(parsed_link))

        with database.atomic() as transaction:
            try:
                if parsed_url:
                    site = Site.create(netloc=parsed_url[1])
                except IntegrityError:
                    site_obj = Site.get(netloc=self.url[1])