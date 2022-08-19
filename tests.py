import unittest
from secrets import Secrets
from geneanet import Geneanet
from familysearch import FamilySearch
import json

class SecretsTestCase(unittest.TestCase): 
    def test_secrets_are_initiate(self): 
        """Check if the secrets are initiate"""
        assert Secrets().secrets['geneanet'] is not None
        
    def test_secrets_file_write(self): 
        """Check if the secrets file is write"""
        sec = Secrets()
        sec.save()
        cookie_save = sec.secrets['geneanet']['cookie']
        sec.secrets['geneanet']['cookie'] = "test"
        sec.write()
        self.assertEqual(sec.read()['geneanet']['cookie'], "test")
        sec.secrets['geneanet']['cookie'] = " /\n e#'@ ^ ¨*$ "
        sec.write()
        self.assertEqual(sec.read()['geneanet']['cookie'], " /\n e#'@ ^ ¨*$ ")
        sec.restore() # restore the secrets.yml file to its original state
        self.assertEqual(sec.read()['geneanet']['cookie'], cookie_save)
    
class GeneanetTestCase(unittest.TestCase):
    def test_geneanet_is_initiate(self):
        """Check if the geneanet is initiate"""
        self.assertIsInstance(Geneanet(), Geneanet)
    
    def test_download_gedcom(self):
        """Check if the geneanet download gedcom function is working"""
        geneanet = Geneanet()
        self.assertTrue(len(geneanet.family_names) > 0)

class FamilySearchTestCase(unittest.TestCase):
    def test_familysearch_is_initiate(self):
        """Check if the familysearch is initiate"""
        self.assertIsInstance(FamilySearch(), FamilySearch)
    
    def test_get_tree(self):
        """Check if the familysearch download gedcom function is working"""
        familysearch = FamilySearch()
        with open('data/familysearch_tree.json', 'r') as f:
            self.assertEqual(familysearch.get_tree(), json.load(f))
        
    def test_place_autocompletion(self):
        """Check if the familysearch place autocompletion function is working"""
        familysearch = FamilySearch()
        self.assertEqual(familysearch.place_autocompletion(""), [])
        self.assertTrue("Paris, Île-de-France, France" in familysearch.place_autocompletion("Paris"))
        self.assertTrue("Bruxelles, Belgique" in familysearch.place_autocompletion("Bruxelles"))
        self.assertTrue(familysearch.place_autocompletion("Paris", True)[0]['id'] != "")
        self.assertEqual(familysearch.place_autocompletion("mnpldm"), [])
    
    def test_add_person(self):
        """Check if the familysearch add person function is working"""
        familysearch = FamilySearch()
        person['-PARENT-'] = "not existing"
        self.assertEqual(familysearch.add_person(person), ("Le parent n'a pas été trouvé", f"{person['-PARENT-']} n'a pas été trouvé dans l'arbre"))

    
        

if __name__ == '__main__':
    person = {
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
        4: 'Ajouter une personne'}
    unittest.main()