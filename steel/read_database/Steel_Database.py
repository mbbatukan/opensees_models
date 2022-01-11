# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 01:08:26 2021

@author: Mehmet B Batukan
"""

import numpy as np
import pandas as pd
from sys import platform

def Get_Section_Props(shape, section):
#     if platform == 'darwin':
    file = 'SteelSections_W_HSS.xlsx'
#     else:
    data = pd.read_excel(file, sheet_name=shape)

    sec_props = data[data.eq(section).any(axis=1)].to_dict('list')
    return sec_props

if __name__ == '__main__':
    dummy_dict = Get_Section_Props('W', 'W100x19')
    area = dummy_dict.get('A')
    print(area)
