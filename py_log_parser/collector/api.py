import contextlib
import os

import pysftp

from py_log_parser import helpers


@contextlib.contextmanager
def sftp_client(hostname, conf):
    """Context manager based sftp client

    :param hostname: hostname to connect to
    :param conf: different ssh parameters to connect
    :return: pysftp.Connection instance
    """
    cn_opts = pysftp.CnOpts()
    # Turning off known hosts checking
    cn_opts.hostkeys = conf.host_keys_check
    private_key_path = None
    if conf.private_key_path and os.path.exists(conf.private_key_path):
        private_key_path = conf.private_key_path
    password = None if private_key_path else conf.ssh_password
    with pysftp.Connection(
            hostname,
            username=conf.ssh_login,
            password=password,
            private_key=conf.private_key_path,
            cnopts=cn_opts
    ) as sftp_cli:
        yield sftp_cli


def download(hostname, destination, target, conf):
    """Smart download of files or directories

    :param hostname: address of server to download files
    :param destination: the remote directory or file to copy from
    :param target: the local directory or file to copy to
    :param conf: config object with options for sftp client
    :return: None
    """
    with sftp_client(hostname, conf) as sftp:
        destination = sftp.normalize(destination)
        if sftp.isdir(destination):
            sftp.get_r(destination, target, preserve_mtime=True)
        else:
            target = os.path.join(target, destination[1:])
            helpers.make_tree(os.path.dirname(target))
            sftp.get(destination, target, preserve_mtime=True)
