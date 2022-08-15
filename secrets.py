import yaml


class Secrets:
    def __init__(self) -> None:
        self.secrets = {}
        self.read()
        
    def read(self):
        try:
            with(open('secrets.yml', 'r')) as f:
                self.secrets = yaml.safe_load(f)
        except FileNotFoundError:
            print("No secrets.yml file found")
