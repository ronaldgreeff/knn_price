import pandas as pd
from pandas import DataFrame as df
from models import DBReader
import json

class DataObj:

    def __init__(self, css_keys=None):
        self.db = DBReader()

        if not css_keys:
            self.css_keys = self.get_all_keys()

    def get_all_keys(self):
        return [i[0] for i in self.db.q(""" SELECT key from csskey """)]

    def create_pd_from_page(self, page_id):

        # different blocks have different number of computed key/val pairs
        # can't assign column names from row values dynamically using SQL
        # so can't pivot. Want to perform operations on data anyway, so
        # might as well query everything and perform operations during db -> df

        q = """
        SELECT site.netloc, page.url, page.defaults,
        page.window_innerHeight, page.window_innerWidth,
        block.id, block.text, block.top, block.left,
        block.width, block.height, block.label,
        csskey.key, computed.val
        FROM site
        JOIN page ON page.site_id == site.id
        JOIN block ON block.page_id == page.id
        JOIN computed ON computed.block_id == block.id
        JOIN csskey ON csskey.id == computed.key_id
        WHERE page.id == {id}
        """.format(id=page_id)

        data = self.db.q(q)

        # iterate once over data, storing it by block_id
        # d holds page level data - repeated for each block, so fine if over-written
        # temp holds computed keys and vals

        d = {}
        temp = {}
        page_defaults = ''

        for c, row in enumerate(data):

            block_id = row[5]
            page_defaults = row[2]

            d[ block_id ] = {
                'netloc': row[0],
                'url': row[1],
                'page_height': row[3],
                'page_width': row[4],
                'text': row[6],
                'top': row[7],
                'left': row[8],
                'width': row[9],
                'height': row[10],
                'label': row[11],
            }

            if not temp.get(block_id):
                temp[block_id] = {}
            temp[block_id][row[12]] = row[13]

        # iterate over temp index AND css_keys, adding
        # val if val else 0 into each d[index][css_key]

        for i in temp:
            row = temp[i]
            for key in self.css_keys:
                d[i][key] = 0
                val = row.get(key)
                if val:
                    d[i][key] = val

        self.df = df(d).transpose()
        self.page_defaults = json.loads(page_defaults)

        # todo: write tests:
        # print(temp[35]['display'])
        # print(self.df.loc[[35]]['display'])
        # print(len(d))
        # print([len(temp[i]) for i in temp.keys()])
        # print(temp.keys())
        # print(d.keys())
        # print(d[1].keys())
        # print(df(d).transpose())

    def show_css_key_vals(self):
        for css_key in self.css_keys:
            print(self.df.loc[self.df[css_key] != 0][css_key])

    def show_all(self):
        with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
            print(self.df0)

    def pre_process(self):
        pass
