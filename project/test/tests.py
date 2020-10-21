from database import models
from database.db_managers import DBReader as dbr
from crawler import selenium_obj
from database.db_managers import DBWriter as dbw
from data import clusterer, dataframe
from utils import local_files, urls, features

import unittest
import numpy as np
from peewee import *
import json

class TestDBWriter(unittest.TestCase):

    database = 'test.db'
    dbw = DBWriter(database)

    # extract = 'test_extract.json'
    # with open(extract, 'r') as f:
    #     extract = json.loads(f.read())

    # dbw.store_page_extract(
    #     extract = extract,
    #     url = 'https://www.boots.com/loreal-paris-revitalift-filler-serum-30ml-10274580',
    #     purge_record = False,
    # )


class TestDataObj(unittest.TestCase):
    css_keys = ['color', 'font-size', 'font-weight', 'text-transform',
        # 'text-align', 'vertical-align', 'text-shadow', 'font-family',
        ]
    data = DataObj(css_keys=css_keys)
    data.get_dataframes([1,2,3,4,5])
    data.pre_process()
    # print(data.ppdf)
    # print(data.ppdf.head())
    # print(data.ppdf.columns)

# class TestDataObjFunctions(unittest.TestCase):
        # todo: write get_dataframe tests:
        # print(temp[35]['display'])
        # print(self.df.loc[[35]]['display'])
        # print(len(d))
        # print([len(temp[i]) for i in temp.keys()])
        # print(temp.keys())
        # print(d.keys())
        # print(d[1].keys())
        # print(df(d).transpose())


class TestClusterControl(unittest.TestCase):

    def test_get_min_eps_for_cluster(self):
        X = np.array([[1, 2], [2, 2], [2, 3]])
        tci = [0, 1, 2]
        min_samples = len(tci) # since we expect tcis to represent a unique element per page/sample
        step = 0.01

        result = get_min_eps_for_cluster(X, tci, min_samples, step)

        self.assertEqual(result, 1.0)


    def test_get_max_eps_for_cluster(self):
        X = np.array([[1, 0], [1, 0], [5, 0]])
        tci = [0, 1]
        min_samples = len(tci)
        step = 0.01

        result = get_max_eps_for_cluster(X, tci, min_samples, step, label=0, eps=1.0,)

        self.assertEqual(result, 4.0)


    def test_get_cluster_boundaries(self):

        X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80], [95, 105], [105, 95], [100, 100] ])
        tcis = ([0, 1], [2, 3], [5, 6, 7]) # list of X indices that should form true clusters

        result = get_cluster_boundaries(X, tcis)

        pass #todo


class TestUtils(unittest.TestCase):

    def test_str_px_to_float(self):

        poss_vals = ["50px", 50, 50.0]

        for pval in poss_vals:
            result = str_px_to_float(pval)

            self.assertEqual(type(result), type(float()))
            self.assertEqual(result, 50.0)


    def test_rgb_to_coords(self):

        rgb_string = 'rgb(80, 125, 255)'
        r, g, b = rgb_to_coords(rgb_string)
        self.assertEqual([r, g, b], [(80/255), (125/255), (255/255)])


    def test_is_it_color(self):

        colours = (
            ('rgb(255, 0, 0)', 1, 'red',),
            ('rgb(0, 0, 0)', 0, 'black',),
            ('rgb(255, 255, 255)', 0, 'white',),
            ('rgb(0, 255, 0)', 1, 'green',),
            ('rgb(0, 0, 255)', 1, 'blue',),
            ('rgb(255, 128, 128)', 1, 'pink (center top)',),
            ('rgb(25, 13, 13)', 0, 'basically black (center bottom)',),
            ('rgb(128, 115, 115)', 0, 'basically grey (center left)',),
            ('rgb(128, 0, 0)', 1, 'red (mid right)',),
            ('rgb(128, 128, 128)', 0, 'grey (mid left)',),
            ('rgb(128, 64, 64)', 1, '(dead centre)',),
            ('rgb(255, 186, 186)', 1, 'pink left',),
            ('rgb(255, 15, 15)', 1, 'pink right',),
            ('rgb(0, 106, 184)', 1, '$data blue',),
            ('rgb(242, 242, 242)', 0, '$data (white)',),
            ('rgb(89, 88, 89)', 0, '$data darkish grey',),
            ('rgb(102, 102, 102)', 0, '$data lightish grey',),
            ('rgb(194, 194, 194)', 0, '$data light grey',),
            ('rgb(51, 51, 51)', 0, '$data dark grey',),
            ('rgb(77, 38, 38)', 1, '$edge dark red',),
            ('rgb(31, 15, 15)', 1, '$edge darker red/brown',),
            ('rgb(26, 1, 1)', 0, '$edge super dark brown/black',),
            ('rgb(255, 207, 207)', 0, '$edge pink far left',),
            ('rgb(235, 216, 216)', 0, '$edge super light pink/white',),
            ('rgb(230, 200, 200)', 0, '$edge super light pink/white',),
        )

        for rgb, expectation, colour in colours:
            result = is_it_color(rgb)

            if expectation != result:
                print('FAILED: {} exp: {} res: {}'.format(
                    colour, expectation, result))

            self.assertEqual(result, expectation)

    def test_text_to_features(self):

        test_texts = (
            (["Home"], ('Home', 4, 0, 4, 0, 0)),
            (["this is a ", "mega", " sale!"], ('this is a mega sale!', 20, 0, 15, 4, 0)),
            (["why is this paragraph so fricken' long?"], ('why is this paragraph so fricken\' long?', 39, 0, 31, 6, 0)),
            (["£35.00"], ('£35.00', 6, 4, 0, 0, 1)),
            (["£", "35.00"], ('£35.00', 6, 4, 0, 0, 1)),
        )

        for texts, expected in test_texts:
            result = text_to_features(json.dumps(texts))

            self.assertEqual(result, expected)

    def text_transform(self):
        pass

if __name__ == '__main__':
    unittest.main()
