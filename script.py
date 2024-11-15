import numpy as np
import pandas as pd


import rstr, subprocess
from random import randint, choice, uniform


import xmlschema
import xml.etree.cElementTree as ET


eans = pd.read_csv("EAN.txt").T.iloc[0].to_list()
inns = pd.read_csv("INN.txt").T.iloc[0].to_list()


## Bottle
get_bottle = lambda : {
    'price': str(round(uniform(100, 1001), 2)),
    'barcode': rstr.xeger("\d\dN\w{20}\d[0-1]\d[0-3]\d{10}\w{31}") ,
    'ean': str(choice(eans)),
    'volume': str(round(choice(np.linspace(0.1, 3.0, num=59)), 2))
}

## Cheque
get_cheque = lambda : {
    'inn': str(choice(inns)),
    'kpp': rstr.xeger("(\d{9}|)"),
    'address': ''.join([rstr.xeger(f'[а-я]') for _ in range(randint(10, 21))]),
    'name': rstr.xeger('^[A-Za-z0-9]{6,12}$'),
    'kassa': rstr.xeger(f'[A-G]') ,
    'shift': str(randint(0, 10)),
    'number': str(randint(0, 10)),
    'datetime': rstr.xeger(r'[0-3][0-9][0-1][0-9][0-9]{2}[0-2][0-9][0-5][0-9]'),

}



def get_random_cheque():
    
    root = ET.Element("Cheque", **get_cheque())
    
    for _ in range(randint(1, 10)):
        ET.SubElement(root, "Bottle", **get_bottle())
    
    return root



if __name__ == "__main__":
    
    cheque = get_random_cheque()   
    
    if xmlschema.XMLSchema("xsd-схема.xsd").is_valid(cheque):
        
        print("XML file is valid")
    
        ET.ElementTree(cheque).write("cheque.xml")
        
        print('File saved in ./cheque.xml')

        r = subprocess.run(["curl", "-F", "xml_file=@cheque.xml", "http://localhost:8080/xml"], capture_output=True)
    
        if r.returncode == 0:
            print("Curl finished with statuscode: 0")
    
        else:
            print("Curl crashed with statuscode: " + str(r.returncode))