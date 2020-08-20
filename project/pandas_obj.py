import pandas as pd
from pandas import DataFrame as df
from models import DBReader

class DataObj:

    def __init__(self):
        self.db = DBReader()
        # self.df0 = pd.read_sql(query, con)

    def fetch_page(self, page_id=1):
        """
        TODO Store these as global as used by init_df0 too:

        site.netloc,
        page.url, page.window_innerHeight, page.window_innerWidth,
        block.text, block.top, block.left,
        block.width, block.height, block.label,
        csskey.key, computed.val
        """

        qk = """
            SELECT site.netloc, page.url, page.window_innerHeight, page.window_innerWidth, block.text, block.top, block.left, block.width, block.height, block.label, csskey.key, computed.val
            FROM site
            JOIN page ON page.site_id == site.id
            JOIN block ON block.page_id == page.id
            JOIN computed ON computed.block_id == block.id
            JOIN csskey ON csskey.id == computed.key_id
            WHERE page.id == {id}
        """.format(id=page_id)

        return self.db.q(qk)


    def init_df0(self):
        # different blocks have different number of computed key/val pairs
        # can't assign column names from row values dynamically using SQL
        # so can't pivot. Want to perform operations on data anyway, so
        # might as well do it during db > df after querying for everything
        # data = self.fetch_page()

        columns = ['netloc', 'url', 'page_height', 'page_width',
        'text', 'top', 'left', 'width', 'height', 'label'
        ]
        css_keys = [i[0] for i in self.db.q(""" SELECT key from csskey """)]
        ndf = df(columns=(columns+css_keys))

        page_id = 1
        q = """
        SELECT site.netloc, page.url, page.window_innerHeight, page.window_innerWidth,
        block.text, block.top, block.left, block.width, block.height, block.label,
        csskey.key, computed.val
        FROM site
        JOIN page ON page.site_id == site.id
        JOIN block ON block.page_id == page.id
        JOIN computed ON computed.block_id == block.id
        JOIN csskey ON csskey.id == computed.key_id
        WHERE page.id == {id}
        """.format(id=page_id)
        data = pd.read_sql(q, self.db.con())

        for i, row in data.iterrows():
            print(
                row['netloc'],
                row['url'],
                row['window_innerHeight'],
                row['window_innerWidth'],
                row['text'],
                row['top'],
                row['left'],
                row['width'],
                row['height'],
                row['label'],
                row['key'],
                row['val'],
                )

    def show_all(self):
        with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
            print(self.df0)

    def pre_process(self):
        pass
