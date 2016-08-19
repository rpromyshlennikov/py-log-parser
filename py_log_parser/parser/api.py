import logging

from py_log_parser.parser import extractors as ex


logger = logging.getLogger(__name__)


class LogFileParser(object):
    """Class handles parsing of log-files with provided extractors"""

    def __init__(self, input_filename, extractors=(), output_filename=None):
        self.extractors = extractors
        self.extractors_mapping = {extractor.name: extractor
                                   for extractor in self.extractors}
        self.log_file = input_filename
        self.output = self.log_file if not output_filename else output_filename
        self._coroutine_writers = {}
        self._init_write_coroutines(self.extractors_mapping.keys())
        self._extracted_files = []

    def _init_write_coroutines(self, extractor_names):

        def write_coroutine(file_name, data=None):
            data = yield data
            self._extracted_files.append(file_name)
            with open(file_name, "a") as out_file:
                logger.info(
                    "Opened {} file to write result.".format(file_name))
                while data:
                    out_file.write(data)
                    data = yield data

        self._coroutine_writers = {
            name: write_coroutine("{}_{}.txt".format(self.output, name))
            for name in extractor_names
        }
        for coroutine in self._coroutine_writers.values():
            coroutine.send(None)

    def iterate_occurrences(self):
        with open(self.log_file) as log_file:
            for line in log_file:
                for extractor in self.extractors:
                    occurrence = extractor.process(line)
                    if occurrence:
                        yield occurrence, extractor

    def parse_file(self):
        logger.debug("Opened {} file to parse.".format(self.log_file))
        for occurrence, extractor in self.iterate_occurrences():
            self._coroutine_writers[extractor.name].send(occurrence)
        return self._extracted_files


def parse_log_file(filename, extractor_names=("tracebacks",),
                   conf=None, output_filename=None):
    """Function parses provided log file

    :param filename: log file name
    :param extractor_names: collection of extractors to process file
    :param conf: config object with options for extractors
    :param output_filename: output filename to write results
    :return: None
    """
    log_parser = LogFileParser(
        filename,
        extractors=[extractor(conf)
                    for extractor in ex.get_extractors(extractor_names)],
        output_filename=output_filename
    )
    return log_parser.parse_file()
