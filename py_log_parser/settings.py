import os

console_log_level = os.environ.get('LOG_LEVEL', "INFO")

# Extractors settings
tb_ex_stats = os.environ.get("TRACEBACK_EXTRACTOR_STATS", False)
tb_ex_strip_space = os.environ.get("TRACEBACK_EXTRACTOR_STRIP", False)
log_ex_level = os.environ.get("LOGGING_EXTRACTOR_LEVEL", "ERROR")
re_ex_regexp = os.environ.get("RE_EXTRACTOR_REGEXP")

# Ssh settings
ssh_login = os.environ.get("ENV_FUEL_LOGIN", "root")
ssh_password = os.environ.get("ENV_FUEL_PASSWORD", "r00tme")
private_key_path = os.environ.get(
    "FUEL_KEY", os.path.join(os.path.expanduser("~"), "fuel.key"))
host_keys_check = os.environ.get("STRICT_SSH_CHECK", None)

# MOS workflow settings
working_dir = os.environ.get("WORKING_DIR", "/tmp/py_log_parser")
init_dir_path = os.environ.get("INIT_DIR_PATH", "init")
final_dir_path = os.environ.get("FINAL_DIR_PATH", "final")
stripped_dir_path = os.environ.get("STRIPPED_DIR_PATH", "stripped")
parse_input_dir_path = os.environ.get("PARSE_INPUT_DIR_PATH", "input")
parse_output_dir_path = os.environ.get("PARSE_OUTPUT_DIR_PATH", "output")
remote_collect_path = os.environ.get("REMOTE_COLLECT_PATH", "/var/log")
catalog_name = os.environ.get("EXTRACTED_CATALOG_PATH", "catalog.txt")
