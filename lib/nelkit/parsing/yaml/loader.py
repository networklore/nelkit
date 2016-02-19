import os
import yaml
from nelkit.exceptions import FileNotFound, ParsingError


class YamlLoader:

    def __init__(self, filename=None):

        self._filename = filename
        self._load()

    def _load(self):
        if not os.path.isfile(self._filename):
            raise FileNotFound('Unable to read: %s' % self._filename)
        try:
            with open(self._filename) as f:
                self.data = yaml.load(f.read())
        except:
            raise ParsingError('%s is not a valid yaml file' % self._filename)
