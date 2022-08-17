'''This module connects the program to geneanet.org'''

from secrets import Secrets
import requests


headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "www.familysearch.org",
        "Accept": "application/json",
        "Referer": "https://www.familysearch.org/tree/pedigree/portrait/LQ5D-CG9",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers",
    }


class FamilySearch:
    def __init__(self):
        self.secrets = Secrets()
        self.session = requests.Session()
        self.session.headers.update(headers)

    def add_person(self, person):
        '''Add a person to the familysearch database'''
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
        if place == '':
            return []
        response = self.session.get(
            "https://www.familysearch.org/service/tree/tree-data/authorities/place",
            params={"term": place, "locale": "fr"},
            headers={
                "Cookie": self.secrets.secrets['familysearch']['cookie']
            }
        )
        json = response.json()
        return [p['label'] for p in json]

