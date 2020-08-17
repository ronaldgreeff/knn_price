import pandas as pd
from models import DBReader

class DataObj:

    def __init__(self):
        query, con = DBReader().collect_df_data()
        self.df0 = pd.read_sql(query, con)
