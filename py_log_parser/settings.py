import os

console_log_level = os.environ.get('LOG_LEVEL', "INFO")

# Ssh settings
ssh_login = os.environ.get("ENV_FUEL_LOGIN", "root")
ssh_password = os.environ.get("ENV_FUEL_PASSWORD", "r00tme")
private_key_path = os.environ.get(
    "FUEL_KEY", os.path.join(os.path.expanduser("~"), "fuel.key"))
host_keys_check = os.environ.get("STRICT_SSH_CHECK", None)
