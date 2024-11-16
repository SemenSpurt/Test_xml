import numpy as np
import pandas as pd


eans = pd.read_csv("EAN.txt").T.iloc[0].to_list()
inns = pd.read_csv("INN.txt").T.iloc[0].to_list()

schema_path = "./xsd-схема.xsd"


import rstr, re
from random import randint, choice, uniform


cheque_attrs = lambda : {
    'inn'      : str(choice(inns)),
    'kpp'      : rstr.xeger("(\d{9}|)"),
    'shift'    : str(randint(0, 10)),
    'number'   : str(randint(0, 10)),
    'kassa'    : rstr.xeger(f'[A-G]') ,
    'name'     : rstr.xeger('^[A-Za-z0-9]{6,12}$'),
    'address'  : ''.join([rstr.xeger('[а-я]') for _ in range(randint(10, 20))]),
    'datetime' : rstr.xeger('[0-3][0-9][0-1][0-9][0-9]{2}[0-2][0-9][0-5][0-9]'),
}
 

bottle_attrs = lambda : {
    'ean': str(choice(eans)),
    'price': str(round(uniform(100, 1001), 2)),
    'volume': str(round(choice(np.linspace(0.1, 3.0, num=59)), 2)),
    'barcode': rstr.xeger("\d\dN\w{20}\d[0-1]\d[0-3]\d{10}\w{31}"),

}
