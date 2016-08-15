## Introduction

This project created for collecting and parsing logs

### Build

    $ python setup.py sdist

### Install

    $ virtualenv --clear venv
    $ source venv/bin/activate
    $ pip install -U pip
    $ pip install py_log_parser-<version>.tar.gz


### Environment prepare

You should have needed authentication for servers that will be processed.


### Usage

Base parameters:
```
py-log-parser [-h] [--ssh-login SSH_LOGIN]
                     [--ssh-password SSH_PASSWORD]
                     [--private-key-path PRIVATE_KEY_PATH] [--host-keys-check]
                     [--tb-ex-stats] [--tb-ex-strip-space]
                     [--log-ex-level {WARN,ERROR,DEBUG,INFO,WARNING,CRITICAL,NOTSET}]
                     [--re-ex-regexp RE_EX_REGEXP]
                     [--console-log-level {WARN,ERROR,DEBUG,INFO,WARNING,CRITICAL,NOTSET}]
                     {mos} ...

positional arguments:
   {mos}              Different workflows
    mos                 Commands for parsing logs with MOS workflow

optional arguments:
  --ssh-login SSH_LOGIN
                        Ssh client login
  --ssh-password SSH_PASSWORD
                        Ssh client password (not used in case of auth by key)
  --private-key-path PRIVATE_KEY_PATH
                        Ssh client private key path
  --host-keys-check     Enable strict checking of known hosts on ssh
                        connection
  --tb-ex-stats         Collect tracebacks statistic or not
  --tb-ex-strip-space   Strip timestamp in tracebacks or leave it
  --log-ex-level {WARN,ERROR,DEBUG,INFO,WARNING,CRITICAL,NOTSET}
                        Logging level to extract logging messages
  --re-ex-regexp RE_EX_REGEXP
                        Regexp for regular expressions extractor
  --console-log-level {WARN,ERROR,DEBUG,INFO,WARNING,CRITICAL,NOTSET}
                        Logging level to output messages

```
Mos workflow usage:
```
usage: py-log-parser mos [-h] [--working-dir WORKING_DIR]
                         [--init-dir-path INIT_DIR_PATH]
                         [--final-dir-path FINAL_DIR_PATH]
                         [--stripped-dir-path STRIPPED_DIR_PATH]
                         [--parse-input-dir-path PARSE_INPUT_DIR_PATH]
                         [--parse-output-dir-path PARSE_OUTPUT_DIR_PATH]
                         [--remote-collect-path REMOTE_COLLECT_PATH]
                         {collect,analyze,clean,init} ...

positional arguments:
  {collect,analyze,clean,init}
                        Commands for MOS workflow
    collect
    analyze
    clean
    init

optional arguments:
  --working-dir WORKING_DIR
                        Working directory to work with log files
  --init-dir-path INIT_DIR_PATH
                        Directory where files will be placed on <init> command
  --final-dir-path FINAL_DIR_PATH
                        Directory where files will be placed on <collect>
                        command
  --stripped-dir-path STRIPPED_DIR_PATH
                        Directory where stripped log files will be placed for
                        analysis
  --parse-input-dir-path PARSE_INPUT_DIR_PATH
                        Directory where all input log files will be placed
  --parse-output-dir-path PARSE_OUTPUT_DIR_PATH
                        Directory where all resulting output files will be
                        placed
  --remote-collect-path REMOTE_COLLECT_PATH
                        Directory on remote host that will be downloaded for
                        analysis
```
Base MOS workflow commands usage:
```
usage: py-log-parser mos clean [-h] {all,input,collect}

positional arguments:
  {all,input,collect}  Directory to clear
********************************************
usage: py-log-parser mos init [-h] <hostname or IP>

positional arguments:
  <hostname or IP>  Server to collect logs from
********************************************
usage: py-log-parser mos collect [-h] <hostname or IP>

positional arguments:
  <hostname or IP>  Server to collect logs from
********************************************
usage: py-log-parser mos analyze [-h] <extractor> [<extractor> ...]

positional arguments:
  <extractor>  Extractors to process log files, may be any of ['regexp',
               'tracebacks', 'logging']
```

Usage example:
1. Clean input directory to remove not relevant logs, but not results of previous analysis sessions:
   * `$ py-log-parser mos clean input`
2. Collect logs after deployment but before running tests:
   * `$ py-log-parser mos init <some 1st server>`
   * `$ py-log-parser mos init <some 2nd server>` ... and so on
3. Collect logs after running tests:
   * `$ py-log-parser mos collect <some 1st server>`
   * `$ py-log-parser mos collect <some 2nd server>` ... and so on
4. Run log analysis:
   * `$ py-log-parser mos analyze traceback logging`

After running last command there will be created output folder with parsed data.