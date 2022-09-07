import pandas as pd

def format_excel(db: pd.DataFrame):
    with pd.ExcelWriter('./test.xlsx', engine='openpyxl') as xlr:
        for city in db['CITY'].unique():
            tmp_db = db[db['CITY'] == city][['NAMES','ADDRESS','HOURS']]
            url = ((db[db['CITY'] == city]['URL']).unique())[0]
            tmp_db.to_excel(xlr, sheet_name=city, startrow=1, index=False)
            work_sheet = xlr.sheets[city]
            work_sheet['A1'] = url