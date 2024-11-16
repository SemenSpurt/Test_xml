import config

import subprocess, rstr
from random import randint

import xmlschema
import xml.etree.cElementTree as ET



def random_cheque(
    cheque=config.cheque_attrs(),
    bottle=config.bottle_attrs(),
    updates=False,
    n_bottles=10,
    ):
    
    # 1) Create xml root element
    # 2) Create xml subelements
    # -> root
  
    
    root = ET.Element("Cheque", dict(cheque, datetime=updates["datetime"]()) if updates else cheque)
    
    for _ in range(n_bottles): ET.SubElement(root, "Bottle", dict(bottle, barcode=updates["barcode"]()) if updates else bottle)
    
    return root


def validate(cheque):
    
    return xmlschema.XMLSchema(config.schema_path).is_valid(cheque)


def write(cheque, file="cheque.xml", path="./"):
    
    ET.ElementTree(cheque).write(path + file)
    
    print(f"saved in {path + file}")
    
    
def send(xml_file, url="http://localhost:8080/xml"):
    
    r = subprocess.run(f"curl -F xml_file=@{xml_file} {url}".split(), capture_output=True)
    
    print(f"sent to {url} with code {r.returncode}")
    
    return 0 if r.returncode else 1

    
    
def test(updates=dict(), counts=100):
    
    # 1) Create test xml 
    # 2) Validate by xsd
    # 3) Write down file
    # -> curl returncode
        
    rounds = []
    
    failed = 0
    
    while counts:
        
        try:
            rounds.insert(0, validate(random_cheque(updates=updates)))
            
        except:
            failed += 1
        
        finally:
            counts -= 1
            
    print(
        f"""
        {len(rounds) + failed}\ttotal tests
        {sum(rounds)}\tpassed tests
        {len(rounds) - sum(rounds)}\tfailed test
        {failed}\tpattern error
        """)

    
    
    
def main(xml_file="./cheque.xml"):
    
    # 1) Create test xml 
    # 2) Validate by xsd
    # 3) Write down file
    # -> curl returncode
    
    cheque = random_cheque() 
    
    if validate(cheque):
        
        write(cheque)

        return send(xml_file)
        
    else:
        
        print("pattern error")
        
        return False
        

    
    
if __name__ == "__main__":
    
    test_cases = {
        "Date + Barcode" : { 
            "datetime" : lambda : rstr.xeger('[0-3][0-9][0-1][0-9][0-9]{2}[0-2][0-9][0-5][0-9]'),
            "barcode" : lambda : rstr.xeger("\d\dN\w{20}\d[0-1]\d[0-3]\d{10}\w{31}") ,
        },
        
        "New Date + New Barcode" : {
            "datetime" : lambda : rstr.xeger('(((31(0[13578]|1[02])|((29|30)(0[1,3-9]|1[0-2]))|((0[1-9]|1\d|2[0-8])(0[1-9]|1[0-2])))\d{2})|(2902(0[48]|[2468][048]|[13579][26]|00)))([01]\d|2[0-3])[0-5]\d((\+|-)\d{4})?'),
            "barcode" : lambda : rstr.xeger('([1-9]\d{2}|\d([1-9]\d|\d[1-9])){2}([1-9]\d{7}|\d([1-9]\d{6}|\d([1-9]\d{5}|\d([1-9]\d{4}|\d([1-9]\d{3}|\d([1-9]\d{2}|\d([1-9]\d|\d[1-9])))))))(0[1-9]|1[0-2])(1[8-9]|[2-9][0-9])([1-9]\d{2}|\d([1-9]\d|\d[1-9]))[0-9A-Z]{129}|\d\d[a-zA-Z0-9]{21}\d[0-1]\d[0-3]\d{10}[a-zA-Z0-9]{31}|[0-9]{40}')
        },
        
        "New Date + Barcode" : {
            "datetime" : lambda : rstr.xeger('(((31(0[13578]|1[02])|((29|30)(0[1,3-9]|1[0-2]))|((0[1-9]|1\d|2[0-8])(0[1-9]|1[0-2])))\d{2})|(2902(0[48]|[2468][048]|[13579][26]|00)))([01]\d|2[0-3])[0-5]\d((\+|-)\d{4})?'),
            "barcode" : lambda : rstr.xeger("\d\dN\w{20}\d[0-1]\d[0-3]\d{10}\w{31}") ,
        },
        
        "Date + New Barcode" : {
            "datetime" : lambda : rstr.xeger('[0-3][0-9][0-1][0-9][0-9]{2}[0-2][0-9][0-5][0-9]'),
            "barcode" : lambda : rstr.xeger('([1-9]\d{2}|\d([1-9]\d|\d[1-9])){2}([1-9]\d{7}|\d([1-9]\d{6}|\d([1-9]\d{5}|\d([1-9]\d{4}|\d([1-9]\d{3}|\d([1-9]\d{2}|\d([1-9]\d|\d[1-9])))))))(0[1-9]|1[0-2])(1[8-9]|[2-9][0-9])([1-9]\d{2}|\d([1-9]\d|\d[1-9]))[0-9A-Z]{129}|\d\d[a-zA-Z0-9]{21}\d[0-1]\d[0-3]\d{10}[a-zA-Z0-9]{31}|[0-9]{40}')
        }
    }
    
    
    for key, patches in test_cases.items():
        
        
        print(key)
        
        
        test(updates=patches)