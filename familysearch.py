'''This module connects the program to geneanet.org'''

from secrets import Secrets
import requests
import json



headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "www.familysearch.org",
        "Accept": "application/json",
        "Referer": "https://www.familysearch.org/tree/pedigree/portrait/LRCG-SRT",
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
        self.tree = self.get_tree()

    def place_to_send(self, place:str):
        '''Return the place object to send to the API'''
        r = None if place is None else {
            "localizedText": place,
            "normalizedText": place,
            "originalText": place,
            "id": self.place_autocompletion(place, id=True)[0]['id'],
        }
        return r

    def add_person(self, person: dict):
        '''Add a person to the familysearch database'''
        # If input is empty set to None
        for key in person:
            if person[key] == '':
                person[key] = None
        # define all variables needed to add a person
        parent_type = 'Parent' if person['-TYPEPARENT-'] in ('Père de', 'Mère de') else 'Spouse'
        parent = person['-PARENT-']
        firstname = person['-FIRSTNAME-']
        lastname = person['-LASTNAME-']
        sex = 'FEMALE' if person['-SEX-'] == 'F' else 'MALE'
        occupation = person['-OCCUPATION-']
        birthdate = person['-BIRTHDATE-']
        birthplace = person['-BIRTHPLACE-']
        deathdate = person['-DEATHDATE-']
        deathplace = person['-DEATHPLACE-']
        marriagedate = person['-MARRIAGEDATE-']
        marriageplace = person['-MARRIAGEPLACE-']
        partner = person['-PARTNER-']
        num = '1' if sex == 'MALE' else '2'
        operation_type = f'add{parent_type}{num}'
        parent_id = ""
        # If the parent is a person, get the id
        for key in self.tree['persons']:
            if self.tree['persons'][key]['name'] == parent:
                print(f'parent key : {key}')
                parent_id = key
                break
        if parent_id == "":
            print("Parent not found")
            return ("Le parent n'a pas été trouvé", f"{parent} n'a pas été trouvé dans l'arbre")
        
        self.session.headers.update(
            {
                "Host": "www.familysearch.org",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
                "Accept": "application/json",
                "Accept-Language": "en",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.familysearch.org/tree/pedigree/portrait/GFZK-J5P",
                "authorization": "Bearer 6f21eda3-f863-47e6-8b22-40cce275793b-prod",
                "content-type": "application/json",
                "x-fs-timezone": "-120",
                "Origin": "https://www.familysearch.org",
                "Cookie": self.secrets.secrets['familysearch']['add_person_cookie'],
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "trailers",
                "fs-user-agent-chain": "fs-person-search-service.findByNameCall:/tree/pedigree/portrait/LRCG-3TB",
            }
        )
        response = self.session.post(
            "https://www.familysearch.org/service/tree/tree-data/v8/search/by-name-with-spouses",
            params={"locale": "en"},
            headers={
            },
            json={
                "operationType": operation_type,
                "context": "p" if parent_type == "Parent" else "s",
                "existingRelationshipHasTwoParents": False,
                "ignoreAlreadyRelated": False if parent_type == 'Parent' else True,
                "relatedPersonId": parent_id,
                "birthDetails": {
                    "detailsType": "EventDetails",
                    "type": "BIRTH",
                    "date": {"originalText": birthdate}, #17/01/1968
                    "place": self.place_to_send(birthplace),
                },
                "deathDetails": {
                    "detailsType": "EventDetails",
                    "type": "DEATH",
                    "date": {"originalText": deathdate},
                    "place": self.place_to_send(deathplace),
                },
                "genderDetails": {"gender": sex, "detailsType": "GenderDetails"},
                "nameDetails": {
                    "detailsType": "NameDetails",
                    "nameForms": [
                        {
                            "lang": "fr",
                            "script": "ROMAN",
                            "prefixPart": None,
                            "givenPart": firstname,
                            "familyPart": lastname,
                            "suffixPart": None,
                        }
                    ],
                },
            },
        )
        print(response.request.body)
        print(response.status_code, response.text)
        return (response.status_code, response.text)        

    def place_autocompletion(self, place:str, id:bool = False) -> list:
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
                "Cookie": self.secrets.secrets['familysearch']['autocompletion_cookie']
            }
        )
        json = response.json()
        print(json)
        r = json if id else [p['label'] for p in json]
        return r

    def get_tree(self):
        with open('data/familysearch_tree.json', 'r') as f:
            return json.load(f)


if __name__ == "__main__":
    fs = FamilySearch()
    fs.add_person({
        0: None, 
        '-TYPEPARENT-': 'Père de', 
        '-PARENT-': 'Pierre Bauwen', 
        '-COMBOPARENT-': 'Pierre Bauwen', 
        '-FIRSTNAME-': 'Luc', 
        '-LASTNAME-':'Bauwen', 
        '-SEX-': 'H', 
        '-OCCUPATION-': 'prof', 
        1: 'exactement', 
        '-BIRTHDATE-': '14/05/1720', 
        '-BIRTHPLACE-': 'Mouscron, Hainaut, Belgique', 
        '-COMBOBIRTHPLACE-': 'Mouscron, Hainaut, Belgique', 
        2: 'exactement', 
        '-DEATHDATE-': '14/05/1760', 
        '-DEATHPLACE-': 'Mouscadi, Artibonite, Haïti', 
        '-COMBODEATHPLACE-': 'Mouscadi, Artibonite, Haïti', 
        3: 'exactement', 
        '-MARRIAGEDATE-': '18/05/1740', 
        '-MARRIAGEPLACE-': 'Louviers-Nord, Évreux, Eure, Haute-Normandie, France', 
        '-COMBOMARRIAGEPLACE-': 'Louviers-Nord, Évreux, Eure, Haute-Normandie, France', 
        '-PARTNER-': '', 
        '-COMBOPARTNER-': '', 
        4: 'Ajouter une personne'})