import pandas as pd
import numpy as np
from pandas import DataFrame as df
from models import DBReader
import json
import colorsys

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
            print('{}, def:{}\n{}'.format(
                css_key, self.page_defaults[css_key],
                self.df.loc[self.df[css_key] != 0][css_key],
                ))

    def show_all(self):
        with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
            print(self.df0)

    def pre_process(self):

        def rgb_2_1d(rgb_string, sat_thr=0, val_thr_b=0, val_thr_u=1):
            """ figure out the closest centreline of rgb values (mean)
            then for each value figure out the abs distance from centre
            multiply values to get volume. larger volume = more colour
            scale 0 - 1
            """
            rgb = rgb_string[0]
            text = rgb_string[1]
            numbers_as_s = rgb[4:-1]
            numbers_as_l = numbers_as_s.split(', ')
            list_of_numbers = [int(i) for i in numbers_as_l]

            rgb_coords = [(i/255) for i in list_of_numbers]

            hsv = colorsys.rgb_to_hsv(
                r=rgb_coords[0],
                g=rgb_coords[1],
                b=rgb_coords[2],
                )

            hue = hsv[0]
            sat = hsv[1]
            val = hsv[2]

            result = ''

            sat_thr = 0.2
            val_thr_b = 0.2
            val_thr_u = .8

            if sat < sat_thr:
                result = 'n'
            elif val_thr_b < val < val_thr_u:
                result = 'n'

            # print(rgb_coords, hsv)

            print('{} {}: {:.2f}, {:.2f}, {:.2f}'.format(result, text, hue, sat, val))

            # m = np.mean(list_of_numbers)
            # # x = sum([(abs(m-i)/255) for i in list_of_numbers])
            # x = [(abs(m-i)) for i in list_of_numbers]
            # r = sum(x)/m
            # o = 'colour' if r>thresh else 'noir'
            # print(o, text, r, rgb)
            # return r

        thresh = rgb_2_1d(('rgb(255, 222, 222)', 'super light'))
        print('-------')
        for i in (
            ('rgb(0, 0, 0)', 'black',),
            ('rgb(255, 255, 255)', 'white',),
            ('rgb(128, 64, 64)', '(dead centre)',),
            ('rgb(255, 0, 0)', 'red',),
            ('rgb(0, 255, 0)', 'green',),
            ('rgb(0, 0, 255)', 'blue',),
            ('rgb(128, 0, 0)', 'red (mid right)',),
            ('rgb(77, 38, 38)', 'dark red',),
            ('rgb(0, 106, 184)', 'data blue',),
            ('rgb(255, 128, 128)', 'pink (center top)',),
            ('rgb(255, 207, 207)', 'pink far left',),
            ('rgb(255, 186, 186)', 'pink left',),
            ('rgb(255, 15, 15)', 'pink right',),
            ('rgb(128, 128, 128)', 'grey (mid left)',),
            ('rgb(25, 13, 13)', 'basically black (center bottom)',),
            ('rgb(128, 115, 115)', 'basically grey (center left)',),
            ('rgb(242, 242, 242)', 'data (white)',),
            ('rgb(89, 88, 89)', 'data darkish grey',),
            ('rgb(102, 102, 102)', 'data lightish grey',),
            ('rgb(194, 194, 194)', 'data light grey',),
            ('rgb(51, 51, 51)', 'data dark grey',),
        ):
            rgb_2_1d(i)#, thresh=thresh)
