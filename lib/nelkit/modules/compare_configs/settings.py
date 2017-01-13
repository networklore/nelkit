"""Module to compare different configurations files."""
import difflib
import itertools
import os
import re
from glob import glob
from nelkit.exceptions import FileNotFound, NelkitException
from nelkit.parsing.yaml.loader import YamlLoader


class CompareConfigs:
    """Compare configs class, used in nk-compare-configs."""

    def __init__(self, settings_file=None, config_dir=None, baseline=None):
        """Compare configs class, used in nk-compare-configs."""
        self._baseline = baseline
        self._settings = settings_file
        self._config_dir = config_dir
        self.rules = {}
        self._between = {}
        self._num_rules = 0
        self._diff = {}
        self._parse_settings()

        if not self._baseline:
            if len(self._config_files) > 0:
                self._baseline = self._config_files[0]
            else:
                raise FileNotFound('No config files found')

        self._parse_config_files()
        self._parse_sort_rules()
        self._compare_configs()

    def _compare_configs(self):
        for host in self._config_files:
            for rule in self._baseline_matches:
                if self._baseline_matches[rule] != self._matches[host][rule]:
                    node = host.split(os.path.sep)[-1]
                    diff = difflib.unified_diff(
                        self._baseline_matches[rule],
                        self._matches[host][rule],
                        fromfile='baseline',
                        tofile=node)
                    diff = os.linesep.join([x for x in diff])
                    if host not in self._diff.keys():
                        self._diff[host] = {}

                    self._diff[host][rule] = diff

    def _parse_between_rule(self, rule):
        self._num_rules += 1
        if 'start' not in rule.keys():
            raise NelkitException('start key missing in between rule')
        if not isinstance(rule['start'], str):
            raise NelkitException('"start" under between rule has the wrong format')
        match = {}
        match['rule_type'] = 'between'
        match['start'] = rule['start']
        match['start_re'] = re.compile(rule['start'])
        match['end'] = rule.get('end')
        match['sort'] = rule.get('sort')
        match['until_not'] = rule.get('until_not')
        if match['end']:
            match['end_re'] = re.compile(match['end'])
        if match['until_not']:
            match['until_not_re'] = re.compile(match['until_not'])
        match['description'] = rule.get('description')

        if match['end'] and match['until_not']:
            raise NelkitException('"between" rule can not have both end and until_not')
        elif not match['end'] and not match['until_not']:
            raise NelkitException('"between" rule must have end or until_not')

        if 'exclude' in rule.keys():
            match['exclude'] = rule['exclude']
        else:
            match['exclude'] = None
        if match['exclude']:
            match['exclude_re'] = re.compile(match['exclude'])

        self.rules[self._num_rules] = match

    def _parse_configs_dir(self, config_setting, data):

        if config_setting:
            config_dir = config_setting
        else:
            if 'configs' in data.keys():
                config_dir = data['configs']
            else:
                raise NelkitException('config key not found in file')

        if not isinstance(config_dir, list):
            config_dir = [config_dir]

        config_files = []
        for cur_path in config_dir:
            if not os.path.isdir(cur_path):
                raise NelkitException('%s is not a valid config directory' % cur_path)
            if cur_path[-1] != os.path.sep:
                cur_path += os.path.sep
            config_files.append(glob('%s*' % cur_path))
        self._config_files = list(itertools.chain.from_iterable(config_files))

    def _parse_config_files(self):
        self._matches = {}
        for config in self._config_files:
            if config not in self._matches.keys():
                self._matches[config] = {}

            with open(config) as f:
                for line in f:
                    for rule in self.rules:
                        if rule not in self._matches[config].keys():
                            self._matches[config][rule] = []
                        if self.rules[rule]['rule_type'] == 'match':
                            self._run_match_rule(rule, config, line)
                        elif self.rules[rule]['rule_type'] == 'between':
                            self._run_between_rule(rule, config, line)

    def _parse_match_rule(self, rule):
        self._num_rules += 1
        if 'string' not in rule.keys():
            raise NelkitException('string missing in match rule')
        if not isinstance(rule['string'], str):
            raise NelkitException('"string" under match rule has the wrong format')
        match = {}
        match['rule_type'] = 'match'
        match['description'] = rule.get('description')
        match['string'] = rule['string']
        match['string_re'] = re.compile(rule['string'])
        match['sort'] = rule.get('sort')
        if 'exclude' in rule.keys():
            match['exclude'] = rule['exclude']
        else:
            match['exclude'] = None
        self.rules[self._num_rules] = match

    def _parse_settings(self):
        l = YamlLoader(filename=self._settings)
        data = l.data
        self._parse_configs_dir(self._config_dir, data)

        if 'rules' not in data.keys():
            raise NelkitException('rules key not found in file')
        rules = data['rules']

        if not isinstance(rules, list):
            raise NelkitException('rules has to be a list')

        for rule in rules:
            if not isinstance(rule, dict):
                raise NelkitException('rule not a dict!!!!')

            for criteria in rule:
                if not isinstance(rule[criteria], dict):
                    raise NelkitException('NOoOooooo')
                if criteria == 'between':
                    self._parse_between_rule(rule[criteria])
                elif criteria == 'match':
                    self._parse_match_rule(rule[criteria])
                else:
                    raise NelkitException('%s is not a valid rule type' % criteria)

    def _parse_sort_rules(self):

        for host in self._matches:
            for rule in self._matches[host]:
                if self.rules[rule]['sort']:
                    self._matches[host][rule] = sorted(self._matches[host][rule])

        if self._baseline not in self._matches.keys():
            raise NelkitException('Unable to find baseline')
        else:
            self._baseline_matches = self._matches[self._baseline]

    def _run_between_rule(self, rule, config, line):
        if config not in self._between.keys():
            self._between[config] = {}
        if rule not in self._between[config].keys():
            self._between[config][rule] = {}
            self._between[config][rule]['in'] = False
        if self.rules[rule]['end']:
            if self._between[config][rule]['in']:
                if self.rules[rule]['end_re'].match(line):
                    self._between[config][rule]['in'] = False
                if self.rules[rule]['exclude']:
                    if self.rules[rule]['exclude_re'].match(line):
                        return
                self._matches[config][rule].append(line.rstrip())

        if self.rules[rule]['until_not']:
            if self._between[config][rule]['in']:
                if self.rules[rule]['until_not_re'].match(line):
                    if self.rules[rule]['exclude']:
                        if self.rules[rule]['exclude_re'].match(line):
                            return
                    self._matches[config][rule].append(line.rstrip())
                else:
                    self._between[config][rule]['in'] = False

        if self.rules[rule]['start_re'].match(line):
            self._between[config][rule]['in'] = True
            if self.rules[rule]['exclude']:
                exclude = re.compile(self.rules[rule]['exclude'])
                if exclude.match(line):
                    return
            self._matches[config][rule].append(line.rstrip())

    def _run_match_rule(self, rule, config, line):
        if self.rules[rule]['string_re'].match(line):
            if self.rules[rule]['exclude']:
                exclude = re.compile(self.rules[rule]['exclude'])
                if exclude.match(line):
                    return
            self._matches[config][rule].append(line.rstrip())

    def output_diff(self):
        """Print output with diffs."""
        for host in sorted(self._diff.keys()):
            node = host.split(os.path.sep)[-1]
            print('#########################')
            print('# %s' % node)
            print('#########################')
            for rule in self._diff[host]:
                print(self._diff[host][rule])
            print('#########################')
            print('')
