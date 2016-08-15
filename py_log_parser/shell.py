from __future__ import print_function
import argparse
import logging
import sys

from py_log_parser.collector import shell as collector_shell
from py_log_parser.parser import extractors
from py_log_parser.parser import shell as parser_shell
from py_log_parser import settings
from py_log_parser.workflows.mos import shell as mos_shell

logger = logging.getLogger(__name__)


def parse_arguments():

    parser = argparse.ArgumentParser(
        prog="py-log-parser",
        parents=(collector_shell.get_parser(), parser_shell.get_parser())
    )
    parser.add_argument(
        "--console-log-level",
        default=settings.console_log_level,
        choices=extractors.LoggingExtractor.get_logging_levels(True),
        help="Logging level to output messages",
    )
    subparsers = parser.add_subparsers(dest="action_module",
                                       help="Different workflows")
    mos_shell.register_sub_parser(subparsers)
    args = parser.parse_args()
    args.func(args)


def main():
    try:
        parse_arguments()
    except Exception as exc:
        logger.debug(exc, exc_info=1)
        print(
            "ERROR ({type}): {msg}".format(type=exc.__class__.__name__,
                                           msg=exc),
            file=sys.stderr
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print("... terminating py log parser", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
