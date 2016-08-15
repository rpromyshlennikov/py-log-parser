import argparse

from py_log_parser.parser import extractors
from py_log_parser import settings


def get_parser():
    parse_api_parser = argparse.ArgumentParser(add_help=False)
    parse_api_parser.add_argument(
        "--tb-ex-stats",
        default=settings.tb_ex_stats,
        help="Collect tracebacks statistic or not",
        action="store_true"
    )
    parse_api_parser.add_argument(
        "--tb-ex-strip-space",
        default=settings.tb_ex_strip_space,
        help="Strip timestamp in tracebacks or leave it",
        action="store_true",
    )
    parse_api_parser.add_argument(
        "--log-ex-level",
        default=settings.log_ex_level,
        choices=extractors.LoggingExtractor.get_logging_levels(True),
        help="Logging level to extract logging messages",
    )
    parse_api_parser.add_argument(
        "--re-ex-regexp",
        default=settings.re_ex_regexp,
        help="Regexp for regular expressions extractor",
    )
    return parse_api_parser
