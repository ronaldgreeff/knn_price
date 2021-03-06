import pandas as pd
import numpy as np
from pandas import DataFrame as df
import json
from models import DBReader
from utils import (str_px_to_float, is_it_color, rgb_to_coords,
    text_to_features, )

class DataObj:

    def __init__(self, css_keys=None):
        self.db = DBReader()
        self.css_keys = css_keys if css_keys else self.get_all_keys()

    def get_all_keys(self):
        return [i[0] for i in self.db.q(""" SELECT key from csskey """)]

    def get_dataframe(self, page_id):

        data = self.db.query_page(page_id)

        # iterate once over data, storing it by block_id
        # d holds page level data - repeated for each block, so fine if over-written,
        # just collapses into a single row + rest needs to be iterated over anyway
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
        # each d[index][css_key] = val if val else page_default

        self.page_defaults = json.loads(page_defaults)

        for i in temp:
            row = temp[i]
            for key in self.css_keys:
                d[i][key] = self.page_defaults[key]
                val = row.get(key)
                if val:
                    d[i][key] = val

        return df(d).transpose()


    def get_dataframes(self, page_ids):
        dfs = []
        for page_id in page_ids:
            dfs.append(self.get_dataframe(page_id))

        self.df = pd.concat(dfs)

    # Info utils #

    def show_css_key_vals(self):
        for css_key in self.css_keys:
            print('{}, def:{}\n{}'.format(
                css_key, self.page_defaults[css_key],
                (self.df.loc[self.df[css_key] != 0][css_key]),
                ))

    def show_all(self, df):
        with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
            print(df)

    # Preprocess #

    def pre_process(self):

        def text_features_to_pd_series(texts):
            text, len, digits, chars, spaces, denom = text_to_features(texts)
            return pd.Series({
                'str': text,
                'len': len,
                'chars': (chars/len),
                'digits': (digits/len),
                'spaces': (spaces/len),
                'denom': denom, })

        def text_transform(ttv):
            return 1 if ttv == 'capitalize' or ttv == 'uppercase' else 0

        dflt_font_size = str_px_to_float(self.page_defaults['font-size'])
        dflt_font_weight = int(self.page_defaults['font-weight'])

        ndf = self.df['text'].apply(text_features_to_pd_series)
        ndf['label'] = self.df['label']
        ndf['color'] = self.df['color'].apply(is_it_color)
        ndf['font-size'] = self.df['font-size'].apply(str_px_to_float) / dflt_font_size
        ndf['font-weight'] = self.df['font-weight'].astype(int) / dflt_font_weight
        ndf['text-transform'] = self.df['text-transform'].apply(text_transform)
        ndf['x'] = (self.df['top'] + (self.df['height']/2) ) / self.df['page_height']
        ndf['y'] = (self.df['left'] + (self.df['width']/2) ) / self.df['page_width']
        ndf['v'] = (self.df['width']/self.df['page_width'])*(self.df['height']/self.df['page_height'])

        self.ppdf = ndf
