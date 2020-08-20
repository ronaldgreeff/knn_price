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

        # columns = ['netloc', 'url', 'page_height', 'page_width',
        # 'text', 'top', 'left', 'width', 'height', 'label'
        # ]
        # ndf = {k: [] for k in columns}

        css_keys = [i[0] for i in self.db.q(""" SELECT key from csskey """)]

        page_id = 1
        q = """
        SELECT site.netloc, page.url, page.window_innerHeight, page.window_innerWidth,
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
        # data = pd.read_sql(q, self.db.con())
        # print(data.columns)

        data = self.db.q(q)

        d = {}
        temp = {}
        for c, row in enumerate(data):
            block_id = row[4]
            d[ block_id ] = {
                # 'block_id': block_id,
                'netloc': row[0],
                'url': row[1],
                'page_height': row[2],
                'page_width': row[3],
                'text': row[5],
                'top': row[6],
                'left': row[7],
                'width': row[8],
                'height': row[9],
                'label': row[10],
            }
            if not temp.get(block_id):
                temp[block_id] = {}

            temp[block_id][row[11]] = row[12]

        print([len(temp[i]) for i in temp.keys()])
        print(temp.keys())
        print(d.keys())
        # ndf = {'block_id': int(),'netloc': [],'url': [], 'page_height': [],
        # 'page_width': [],'text': [],'top': [],'width': [],'height': [],
        # 'label': [],}

        # process:
        # d1 = {"block_id": [v,...], ... | "css_key": [v, ...]}
        # d2 = {"block_id": {csskey: v}} -> d3 = {"block_id": {csskey: [validated_list]}}
        # d1['block_id'][ d3['block_id'] ] = d3['block_id']['csskey']

        # temp = {}
        # for i, row in data.iterrows():
        #
        #     # ndf['block_id'].append(row['block_id'])
        #     ndf['netloc'].append(row['netloc'])
        #     ndf['url'].append(row['url'])
        #     ndf['page_height'].append(row['window_innerHeight'])
        #     ndf['page_width'].append(row['window_innerWidth'])
        #     ndf['text'].append(row['text'])
        #     ndf['top'].append(row['top'])
        #     ndf['width'].append(row['left'])
        #     ndf['height'].append(row['height'])
        #     ndf['label'].append(row['label'])
        #
        #     block_id = row['id']
        #     if not temp.get(block_id):
        #         temp[block_id] = {}
        #
        #     temp[block_id][row['key']] = row['val']
        #
        #     # if not temp[i]:
        #     #     temp[i] = {}
        #     #     if not temp[i][row['key']]:
        #     #         temp[i][row['key']]
        #     #
        #     # try:
        #     #     temp[i][row['key']] = row['val']
        #     # except KeyError:
        #     #     try:
        #     #         temp[i] = {}
        #     #         temp[i][row['key']] += row['val']
        #     #     except KeyError:
        #     #         temp[i][row['key']] = {}
        #     #         temp[i][row['key']] += row['val']
        #
        #
        # print(temp[0])
        #
        # print(len(ndf['netloc']))
        # print(len(ndf['label']))



    def show_all(self):
        with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
            print(self.df0)

    def pre_process(self):
        pass
