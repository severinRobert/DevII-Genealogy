# DevII-Genealogy
## What is it ?
This is a project for a python course. The goal is to create an app that will centralise several genealogy platform like Geneanet, FamilySearch and Heredis. 

## Run project
* Create a secrets.yml with this content : 
```
geneanet:
  cookie: ""
  sourcename: ""
familysearch:
  cookie: ""
  
```
* Add to it the data required 
* I recommend you to create a virtual environment with `python -m venv ./venv`, executed in the DevII-Genealogy directory. `source ./venv/bin/activate` to active the venv on Linux/Mac or `env\Scripts\activate.bat`.
* Install depedencies with `pip install -r requirements.txt`
* Now copy this code in `./venv/lib/python3.8/site-packages/gedcom/parser.py` at line 144.
```
for line in gedcom_file:
            try:
                last_element = self.__parse_line(line_number, line.decode('utf-8-sig', errors='strict'), last_element, strict)
            except UnicodeDecodeError:
                if not strict:
                    #print('UnicodeDecodeError found:', line_number, line)
                    try:
                        last_element = self.__parse_line(line_number, line.decode('utf-8-sig', errors='replace'), last_element, strict)
                    except:
                        #print('  replace error:', line_number, line)
                        raise
                else:
                    raise
            line_number += 1
```
