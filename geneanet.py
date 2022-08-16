import requests
from secrets import Secrets
import os
from zipfile import ZipFile
from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement


headers = {
        "Host": "gw.geneanet.org",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://gw.geneanet.org",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

class Geneanet:
    def __init__(self):
        self.secrets = Secrets()
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.cookies['cookie'] = self.secrets.secrets["geneanet"]["cookie"]
        self.family_names = []
        
    def add_person(self, person):
        pass

    # return a list of places matching the search term
    def location_autocompletion(self, location):
        r = self.session.post("https://gw.geneanet.org/setup/api/index.php",
                params={
                    "sourcename": self.secrets.secrets["geneanet"]["sourcename"],
                    "type": "w",
                    "lang": "en",
                    "iz": "6",
                    "arbre": "autocomplete",
                },
                headers={
                    "Cookie": self.secrets.secrets["geneanet"]["cookie"]
                },
                data={"data": f"%08%02%10%01%1A%01{location}%20%14"},
            )
        print(r.content.split(b'\n'))
        return r.content.split(b'\n')

    # return a list of individuals matching the search term
    def person_autocompletion(self, person):
        if self.family_names == []:
            self.__download_gedcom()
            gedcom_parser = Parser()
            gedcom_parser.parse_file("data/base.ged", False)
            child_elements = gedcom_parser.get_root_child_elements()
            for element in child_elements:
                if isinstance(element, IndividualElement):
                    (first, last) = element.get_name()
                    self.family_names.append(f'{first} {last}')
        return [name for name in self.family_names if name.upper().startswith(person.upper())] if person != "" else []
    
    # download the gedcom file from geneanet
    def __download_gedcom(self):
        r = self.session.get(
            "https://my.geneanet.org/arbre/save.php",
            params={"view": "save", "action": "save", "typefile": "arbre", "status": "done"},
            headers={
                "Host": "my.geneanet.org",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Connection": "keep-alive",
                "Referer": "https://my.geneanet.org/arbre/save.php?view=save",
                "Cookie": self.secrets.secrets["geneanet"]["cookie"],
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
            },
        )

        file = open("ged.zip", "w+b")
        file.write(r.content)
        file.close

        ZipFile("ged.zip").extractall("data")
        os.remove("ged.zip")

