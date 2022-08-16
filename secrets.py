import yaml


class Secrets:
    def __init__(self, path:str = "data/") -> None:
        self.secrets = {"geneanet": {"cookie": "", "sourcename": ""}, "familysearch": {"cookie": ""}}
        self.path = path
        self.read()
        
    # read the secrets.yml file and update the current secrets or create a new secrets.yml file if it doesn't exist
    def read(self, file:str = f'{self.path}secrets.yml') -> dict:
        try:
            with(open(file, 'r')) as f:
                self.secrets = yaml.safe_load(f)
        # If secrets.yml doesn't exist, create it
        except FileNotFoundError:
            with(open(f'{self.path}secrets.yml', 'w')) as f:
                yaml.dump(self.secrets, f)
        finally:
            return self.secrets

    # write the secrets.yml file with the current secrets
    def write(self, file:str = f'{self.path}secrets.yml') -> None:
        with(open(file, 'w')) as f:
            yaml.dump(self.secrets, f) 

    # save a backup of the current secrets.yml file
    def save(self) -> None:
        self.write(f'{self.path}secrets.yml.back')

    # restore the backup of the secrets.yml.back file
    def restore(self) -> None:
        self.read(f'{self.path}secrets.yml.back')
        self.write()
