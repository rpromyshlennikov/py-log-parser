import logging
import os
import shutil
import time

from py_log_parser.collector import api as collector_api
from py_log_parser import exceptions
from py_log_parser import helpers
from py_log_parser.parser import api as parser_api


logger = logging.getLogger(__name__)


class MosWorkflow(object):
    """Class that implements needed methods for mos workflow log parsing"""
    instance = None

    @classmethod
    def get_mos_workflow(cls, config):
        if MosWorkflow.instance is None:
            MosWorkflow.instance = MosWorkflow(config)
        return MosWorkflow.instance

    def __init__(self, config):
        self.config = config
        self._working_dir = self.config.working_dir
        self._input_dir = os.path.join(self._working_dir,
                                       config.parse_input_dir_path)
        self._remote_collect_path = self.config.remote_collect_path
        self._init_dir = os.path.join(self._input_dir, config.init_dir_path)
        self._collect_dir = os.path.join(self._input_dir,
                                         config.final_dir_path)
        self._stripped_dir = os.path.join(self._input_dir,
                                          config.stripped_dir_path)
        self._output_dir = os.path.join(self._working_dir,
                                        config.parse_output_dir_path)

    def _make_working_dir(self):
        """Makes working directory"""
        helpers.make_tree(self._working_dir)

    def clean(self, name):
        """Clean working directories

        :param name: name of directory to clean
        :return: None
        """
        dirs = {
            "input": self._input_dir,
            "collect": self._collect_dir,
            "all": self._working_dir,
        }
        try:
            helpers.remove_tree(dirs[name])
        except KeyError:
            msg = (
                "Provided dir ({name}) is not available, "
                "please, choose from next values: {keys}".format(
                    name=name, keys=dirs.keys())
            )
            logger.error(msg)
            raise KeyError(msg)

    def init(self, hostname):
        """Collects logs on initial state (before tests)

        :param hostname: hostname to collect from
        :return: None
        """
        self._make_working_dir()
        path = os.path.join(self._init_dir, hostname)
        helpers.make_tree(path)
        collector_api.download(
            hostname, self._remote_collect_path, path, self.config)

    def collect(self, hostname):
        """Collects logs on final state (after the tests)

        :param hostname: hostname to collect from
        :return: None
        """
        self._make_working_dir()
        path = os.path.join(self._collect_dir, hostname)
        helpers.make_tree(path)
        collector_api.download(
            hostname, self._remote_collect_path, path, self.config)

    def _prepare_diff_logs(self):
        """Prepare log files for analysis

        Make decision which file need to send to parser.
        """
        helpers.make_tree(self._stripped_dir)
        for (dirpath, _, filenames) in os.walk(self._collect_dir):
            for filename in filenames:
                abs_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(abs_path, self._collect_dir)
                init_file_path = os.path.join(self._init_dir, rel_path)
                stripped_file_path = os.path.join(self._stripped_dir, rel_path)
                helpers.make_tree(os.path.dirname(stripped_file_path))
                if os.path.exists(init_file_path):
                    try:
                        helpers.strip_file(
                            init_file_path, abs_path, stripped_file_path)
                    except exceptions.FilesMismatchError as e:
                        logger.exception(e)
                else:
                    shutil.copy2(abs_path, stripped_file_path)

    def analyze(self, extractors):
        """Parse prepared logs and store result"""
        self._prepare_diff_logs()
        output_dir = os.path.join(
            self._output_dir, "{}".format(time.strftime("%Y_%m_%d_%H_%M_%S")))
        for (dirpath, _, filenames) in os.walk(self._stripped_dir):
            for filename in filenames:
                abs_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(abs_path, self._stripped_dir)
                output_filename = os.path.join(output_dir, rel_path)
                helpers.make_tree(os.path.dirname(output_filename))
                parser_api.parse_log_file(
                    abs_path, extractors, self.config, output_filename)
