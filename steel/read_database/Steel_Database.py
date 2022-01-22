#%%
import pandas as pd

def Get_Section_Props(shape, section):
    file = 'SteelSections_W_HSS.xlsx'
    data = pd.read_excel(file, sheet_name=shape).set_index("Dsg")
    return data.loc[section]

if __name__ == '__main__':
    series_dummy = Get_Section_Props('W', 'W100x19')
    area = series_dummy["A"]
    print(area)