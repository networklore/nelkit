from nelkit.exceptions import FileNotFound, ParsingError
from nelkit.parsing.yaml.loader import YamlLoader
import pytest

def test_YamlLoader():
    yl = YamlLoader(filename='tests/parsing/yaml/data/base.yml')
    assert isinstance(yl.data, dict)


def test_load_missing_file():
    with pytest.raises(FileNotFound) as excinfo:
        yl = YamlLoader(filename='tests/parsing/yaml/data/file_that_does_not_exist.yml')
    assert 'Unable to read: tests/parsing/yaml/data/file_that_does_not_exist.yml' == str(excinfo.value)


def test_load_invalid_file():
    with pytest.raises(ParsingError) as excinfo:
        yl = YamlLoader(filename='tests/parsing/yaml/data/invalid_yaml.yml')
    assert 'tests/parsing/yaml/data/invalid_yaml.yml is not a valid yaml file' == str(excinfo.value)
