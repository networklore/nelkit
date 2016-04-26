"""Tests to validate yaml features."""
from nelkit.exceptions import FileNotFound, ParsingError
from nelkit.parsing.yaml.loader import YamlLoader
import pytest


def test_YamlLoader():
    """Test to see that the YamlLoader returns a dict."""
    yl = YamlLoader(filename='tests/parsing/yaml/data/base.yml')
    assert isinstance(yl.data, dict)


def test_load_missing_file():
    """Test to verify that an exception is raised when trying to load a non-existing file."""
    with pytest.raises(FileNotFound) as excinfo:
        YamlLoader(filename='tests/parsing/yaml/data/file_that_does_not_exist.yml')
    assert 'Unable to read: tests/parsing/yaml/data/file_that_does_not_exist.yml' == str(excinfo.value)


def test_load_invalid_file():
    """Test to verify that an exception is raised when the yaml file is invalid."""
    with pytest.raises(ParsingError) as excinfo:
        YamlLoader(filename='tests/parsing/yaml/data/invalid_yaml.yml')
    assert 'tests/parsing/yaml/data/invalid_yaml.yml is not a valid yaml file' == str(excinfo.value)
