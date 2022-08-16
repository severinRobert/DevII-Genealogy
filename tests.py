import unittest
from secrets import Secrets

class SecretsTestCase(unittest.TestCase): 
    def test_secrets_are_initiate(self): 
        """Check if the secrets are initiate"""
        assert Secrets().secrets['geneanet'] is not None
        
    def test_secrets_file_write(self): 
        """Check if the secrets file is write"""
        sec = Secrets()
        save = sec.secrets
        sec.secrets['geneanet']['cookie'] = "test"
        sec.write()
        self.assertEqual(sec.read()['geneanet']['cookie'], "test")
        sec.secrets['geneanet']['cookie'] = " /\n e#'@ ^ ¨*$ "
        sec.write()
        self.assertEqual(sec.read()['geneanet']['cookie'], " /\n e#'@ ^ ¨*$ ")
        sec.restore() # restore the secrets.yml file to its original state
        self.assertEqual(sec.read()['geneanet']['cookie'], save['geneanet']['cookie'])
    
class RequestsTestCase(unittest.TestCase):
    pass
        

if __name__ == '__main__':
    unittest.main()