'''This module connects the program to geneanet.org'''

from secrets import Secrets
import os
from zipfile import ZipFile
import requests
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
        self.person_autocompletion("")

    def add_person(self, person):
        '''Add a person to the geneanet database'''
        parent = person['-PARENT-']
        firstname = person['-FIRSTNAME-']
        lastname = person['-LASTNAME-']
        sex = person['-SEX-']
        occupation = person['-OCCUPATION-']
        birthdate = person['-BIRTHDATE-']
        birthplace = person['-BIRTHPLACE-']
        deathdate = person['-DEATHDATE-']
        deathplace = person['-DEATHPLACE-']
        marriagedate = person['-MARRIAGEDATE-']
        marriageplace = person['-MARRIAGEPLACE-']
        partner = person['-PARTNER-']

    def place_autocompletion(self, place:str):
        '''Return a list of places matching the search term

            Args:
                place (str): The search term

            Returns:
                list: A list of places matching the search term
        '''
        response = self.session.post("https://gw.geneanet.org/setup/api/index.php",
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
                              data={
                                  "data": f"%08%02%10%01%1A%01{place}%20%14"},
                              )
        print(response.content.split(b'\n'))
        place_list = response.content.split(b'\n')
        return place_list if place_list[0] != b'' else place_list[1:]

    def person_autocompletion(self, person:str):
        '''Return a list of individuals matching the search term

            Args:
                person (str): The search term

            Returns:
                list: A list of individuals matching the search term
        '''
        if not self.family_names:
            self.__download_gedcom()
            gedcom_parser = Parser()
            gedcom_parser.parse_file("data/base.ged", False)
            child_elements = gedcom_parser.get_root_child_elements()
            for element in child_elements:
                if isinstance(element, IndividualElement):
                    (first, last) = element.get_name()
                    self.family_names.append(f'{first} {last}')
        return [name for name in self.family_names if name.upper(
        ).startswith(person.upper())] if person != "" else []

    def __download_gedcom(self):
        '''Download the gedcom file from geneanet'''
        response = self.session.get(
            "https://my.geneanet.org/arbre/save.php",
            params={
                "view": "save",
                "action": "save",
                "typefile": "arbre",
                "status": "done"},
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

        with open("ged.zip", "w+b") as f:
            f.write(response.content)

        ZipFile("ged.zip").extractall("data")
        os.remove("ged.zip")
