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
    url = CharField(null=False, unique=True)
    visited = BooleanField(default=False)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())
    label = CharField(null=True)
    is_sale = BooleanField(null=True)

class Block(BaseModel):
    page = ForeignKeyField(Page, on_delete='CASCADE')
    text = CharField(max_length=64)
    html = CharField(max_length=64)
    label = CharField(null=True)
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


class DBWriter():
    
    def __init__(self):
        """ build db """

        database.connect()
        with database:
            database.create_tables([Site, Page, Block, CSSKey, Computed])
        database.close()

    def clean_links(self, netloc, links):
        """ returns only links that match netloc/domain provided """
        cleaned_links = []
        for link in links:
            parsed_link = urlparse(link)
            if parsed_link[1] == netloc:
                cleaned_links.append(urlunparse(parsed_link))

        return cleaned_links

    def store_page_extract(self, url, extract, purge_record=True):
        """ store the extract """
        parsed_url = urlparse(url)
        clean_url = urlunparse(parsed_url) # remove url clutter

        cleaned_links = self.cleaned_links(parsed_url[1], extract['links'])

        with database.atomic() as transaction:

            try:
                site_obj = Site.create(netloc=parsed_url[1])
            except IntegrityError:
                site_obj = Site.get(netloc=parsed_url[1])

            try:
                page_obj = Page.get(url=clean_url)
                if purge_record:
                    page_obj.delete_instance(recursive=True)
            except Page.DoesNotExist:
                page_obj = Page.create(
                    site=site_obj,
                    url=clean_url,)

            for link in cleaned_links:
                try:
                    Page.create(
                        site=site_obj,
                        url=link)
                except IntegrityError:
                    pass

            for block in extract['texts']:

                text = json.dumps(block['text']) # json.dumps(a list)
                bound = block['bound']

                block_obj = Block.create(
                    page=page_obj,
                    text=text,
                    html=block['html'],
                    top=float(bound['top']),
                    left=float(bound['left']),
                    width=float(bound['width']),
                    height=float(bound['height']),)

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