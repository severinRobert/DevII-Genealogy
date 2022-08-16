import yaml


class Secrets:
    def __init__(self, path:str = "data/") -> None:
        self.secrets = {"geneanet": {"cookie": "", "sourcename": ""}, "familysearch": {"cookie": ""}}
        self.path = path
        self.read()
        self.save()
        
    def read(self, file:str = None) -> dict:
        '''Read the secrets.yml file and update the current secrets or create a new secrets.yml file if it doesn't exist

            Args:
                file (str): The path to the secrets.yml file

            Returns:
                dict: The secrets
        '''
        file = f'{self.path}secrets.yml' if file is None else file
        try:
            with(open(file, 'r')) as f:
                self.secrets = yaml.safe_load(f)
        # If secrets.yml doesn't exist, create it
        except FileNotFoundError:
            with(open(f'{self.path}secrets.yml', 'w')) as f:
                yaml.dump(self.secrets, f)
        finally:
            return self.secrets

    def write(self, file:str = None) -> None:
        '''Write the secrets.yml file with the current secrets

            Args:
                file (str): The path to the secrets.yml file
        '''
        file = f'{self.path}secrets.yml' if file is None else file
        with(open(file, 'w')) as f:
            yaml.dump(self.secrets, f) 

    def save(self) -> None:
        '''Save a backup of the current secrets.yml file'''
        self.write(f'{self.path}secrets.yml.back')

    def restore(self) -> None:
        '''Restore the backup of the secrets.yml file'''
        self.read(f'{self.path}secrets.yml.back')
        self.write()
