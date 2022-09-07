import pandas as pd
import os

def format_excel(db: pd.DataFrame):
    if not os.path.exists("./data"):
        os.makedirs("./data")

    with pd.ExcelWriter('./data/sexshop_data.xlsx', mode="w", engine='openpyxl') as xlr:
        for city in db['CITY'].unique():
            tmp_db = db[db['CITY'] == city][['NAMES','ADDRESS','HOURS']]
            url = ((db[db['CITY'] == city]['URL']).unique())[0]
            tmp_db.to_excel(xlr, sheet_name=city, startrow=1, index=False)
            work_sheet = xlr.sheets[city]
            work_sheet['A1'] = url