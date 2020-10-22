from .models import database, Site, Page, Block, CSSKey, Computed

from utils import urls
from peewee import *
import json

class DBWriter():
    """ Manages writing to db including initial setup of tables """

    def __init__(self, db_abs_path):
        """ build db """

        database.init(db_abs_path)

        database.connect()
        with database:
            database.create_tables([Site, Page, Block, CSSKey, Computed])
        database.close()

        self.database = database

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

        with self.database.atomic() as transaction:
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
#
# class DBReader():
#     # def __init__(self, database=''):
#     #     self.database = database if database else SqliteDatabase('database.db')
#
#     def query_page(self, page_id):
#         """ executes sql query, fetches all data for page_id.
#         Different blocks have different number of computed key/val pairs
#         can't assign column names from row values dynamically using SQL
#         so can't pivot. Want to perform operations on data anyway, so
#         might as well query everything and perform operations during db -> df
#         """
#
#         q = """
#         SELECT site.netloc, page.url, page.defaults,
#         page.window_innerHeight, page.window_innerWidth,
#         block.id, block.text, block.top, block.left,
#         block.width, block.height, block.label,
#         csskey.key, computed.val
#         FROM site
#         JOIN page ON page.site_id == site.id
#         JOIN block ON block.page_id == page.id
#         JOIN computed ON computed.block_id == block.id
#         JOIN csskey ON csskey.id == computed.key_id
#         WHERE page.id == {id}
#         """.format(id=page_id)
#
#         cursor = self.database.execute_sql(q)
#         return cursor.fetchall()
#
#     def data_to_dict(self, data):
#         pass
#
#     def fetch_page_data(self, page_id):
#
#         data = query_page(page_id)
#         # todo
