import argparse

from py_log_parser import settings


def get_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--ssh-login",
        default=settings.ssh_login,
        help="Ssh client login",
    )
    parser.add_argument(
        "--ssh-password",
        default=settings.ssh_password,
        help="Ssh client password (not used in case of auth by key)",
    )
    parser.add_argument(
        "--private-key-path",
        default=settings.private_key_path,
        help="Ssh client private key path",
    )
    parser.add_argument(
        "--host-keys-check",
        default=settings.host_keys_check,
        help="Enable strict checking of known hosts on ssh connection",
        action="store_true"
    )
    return parser
