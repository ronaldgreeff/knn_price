import pandas as pd
from models import DBReader

class DataObj:

    def __init__(self):
        query, con = DBReader().initial_df_data()
        self.df0 = pd.read_sql(query, con)

    def show(self):
        with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
            print(self.df0)
