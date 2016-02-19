
from nelkit.modules.compare_configs.settings import CompareConfigs


BASE_RULES = 'tests/modules/compare_configs/data/base_rules.yml'


def test_base_function():
    CompareConfigs(settings_file=BASE_RULES)
    assert True
