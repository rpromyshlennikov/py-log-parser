import abc
import collections
import logging
import re


class BaseExtractor(object):
    """Base class for extractors"""
    name = None

    def __init__(self):
        assert self.name.replace("_", "").isalnum()

    @abc.abstractmethod
    def process(self, line):
        """Method to process provided line"""
        raise NotImplementedError


class TracebackExtractor(BaseExtractor):
    """Extracts tracebacks from provided line sequence"""
    name = "tracebacks"
    tb_head = "Traceback (most recent call last):"
    tracebacks = collections.defaultdict(int)

    def __init__(self, config=None):
        super(TracebackExtractor, self).__init__()
        self.tb = self.index = None
        self.stats = getattr(config, "tb_ex_stats", False)
        self.strip_space = getattr(config, "tb_ex_strip_space", False)

    def process(self, line):
        if self.tb:
            if line:
                line = line[self.index:]
                self.tb += line
                if line and line[0] != " ":
                    tb = self.tb
                    self.tb = None
                    if self.stats:
                        self.tracebacks[tb[self.index]] += 1
                    return tb
        elif self.tb_head in line:
            self.index = line.index(self.tb_head)
            self.tb = line[self.index:] if self.strip_space else line


class LoggingExtractor(BaseExtractor):
    """Extracts all log messages with provided log level"""
    name = "logging"

    def __init__(self, config=None):
        super(LoggingExtractor, self).__init__()
        self.level = getattr(config, "log_ex_level", "ERROR")
        self.accepted_levels = self._determinate_accepted_levels()

    @classmethod
    def get_logging_levels(cls, only_str=False):
        # pylint: disable=W0212
        level_names = logging._levelNames
        # pylint: enable=W0212
        if only_str:
            return [level for level in level_names.keys()
                    if isinstance(level, str)]
        return level_names

    def _determinate_accepted_levels(self):
        level_names = self.get_logging_levels()
        level = level_names[self.level]
        return [level_names[key] for key in level_names.keys()
                if isinstance(key, int) and key >= level]

    def process(self, line):
        if any(level in line for level in self.accepted_levels):
            return line


class RegExpExtractor(BaseExtractor):
    """Extracts messages by provided regular expression"""
    name = "regexp"

    def __init__(self, config):
        super(RegExpExtractor, self).__init__()
        self.regexp = re.compile(config.re_ex_regexp)

    def process(self, line):
        if self.regexp.search(line):
            return line


def _collect_extractors():
    """Collect all available extractors"""
    ex_classes = [value for value in globals().values()
                  if isinstance(value, type)]
    return [klass for klass in ex_classes
            if issubclass(klass, BaseExtractor) and
            klass != BaseExtractor]


def get_extractors(names=()):
    """Returns list of extractors by if they exists"""
    extractors = _collect_extractors()
    if not names:
        return extractors
    existing_names = {ex.name for ex in extractors}
    if not set(names).issubset(existing_names):
        raise ValueError(
            "Extractor with provided name(s) not found: {names}".format(
                names=", ".join(set(names) - existing_names)
            )
        )
    return [extractor for extractor in _collect_extractors()
            if extractor.name in names]
