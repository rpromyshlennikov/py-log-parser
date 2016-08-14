import errno
import logging
import os
import shutil

from py_log_parser import exceptions

logger = logging.getLogger(__name__)


def strip_file(old_file, updated_file, output_file):
    """Strips file based on comparison between old and updated versions of file

    :param old_file: old file path
    :param updated_file: new file path
    :param output_file: filename to write differences
    :return: None
    """
    logger.info(
        "Stripping file: old - {old}, "
        "updated - {updated}, "
        "stripped - {stripped} ".format(
            old=old_file, updated=updated_file, stripped=output_file)
    )
    with open(output_file, "w") as output:
        with open(old_file) as old, open(updated_file) as updated:
            for line in updated:
                old_line = old.readline()
                if line != old_line:
                    if old_line != "":
                        msg = "Different files were sent to strip"
                        logger.critical(msg)
                        raise exceptions.FilesMismatchError(msg)
                    output.write(line)


def make_tree(path):
    """Makes dir tree if needed

    :param path: full path to directory
    :return: None
    """
    try:
        os.makedirs(path)
        logger.info("Path tree was made: {path}".format(path=path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            logging.exception(e)
            raise
        logger.debug("Path tree exists: {path}".format(path=path))


def remove_tree(path):
    """Removes tree if exist

    :param path:
    :return: None
    """
    try:
        shutil.rmtree(path)
        logger.info("Path tree was removed: {path}".format(path=path))
    except OSError as e:
        if e.errno != errno.ENOENT:
            logging.exception(e)
            raise
        logger.debug("Path tree didn't exist: {path}".format(path=path))
