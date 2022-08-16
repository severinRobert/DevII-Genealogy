import yaml


class Secrets:
    def __init__(self, path:str = "data/") -> None:
        self.secrets = {"geneanet": {"cookie": "", "sourcename": ""}, "familysearch": {"cookie": ""}}
        self.path = path
        self.read()
        
    def read(self) -> dict:
        try:
            with(open(f'{self.path}secrets.yml', 'r')) as f:
                self.secrets = yaml.safe_load(f)
        # If secrets.yml doesn't exist, create it
        except FileNotFoundError:
            with(open(f'{self.path}secrets.yml', 'w')) as f:
                yaml.dump(self.secrets, f)
        finally:
            return self.secrets

    def write(self) -> None:
        with(open(f'{self.path}secrets.yml', 'w')) as f:
            yaml.dump(self.secrets, f)      
