from py_log_parser.parser import api as parser_api
from py_log_parser import settings
from py_log_parser.workflows.mos import api


def arg(*args, **kwargs):
    def wrapper(func):
        def add_args():
            if not hasattr(func, 'arguments'):
                func.arguments = []
            func.arguments.insert(0, (args, kwargs))
        add_args()
        return func
    return wrapper


@arg(
    "name",
    default=None,
    choices=("all", "input", "collect"),
    help="Directory to clear"
)
def do_clean(args):
    mos = api.MosWorkflow.get_mos_workflow(args)
    mos.clean(args.name)


@arg(
    "hostname",
    default=None,
    metavar="<hostname or IP>",
    help="Server to collect logs from"
)
def do_init(args):
    mos = api.MosWorkflow.get_mos_workflow(args)
    mos.init(args.hostname)


@arg(
    "hostname",
    default=None,
    metavar="<hostname or IP>",
    help="Server to collect logs from"
)
def do_collect(args):
    mos = api.MosWorkflow.get_mos_workflow(args)
    mos.collect(args.hostname)


@arg(
    "--catalog-name",
    default=settings.catalog_name,
    help="Extracted files catalog file name"
)
@arg(
    "extractors",
    nargs='+',
    default=[],
    metavar="<extractor>",
    help="Extractors to process log files, may be any of {}".format(
        [ext.name for ext in parser_api.ex.get_extractors()])
)
def do_analyze(args):
    mos = api.MosWorkflow.get_mos_workflow(args)
    mos.analyze(args.extractors, args.catalog_name)


def register_sub_parser(subparsers):
    mos_parser = subparsers.add_parser(
        "mos", help="Commands for parsing logs with MOS workflow")
    mos_parser.add_argument(
        "--working-dir",
        default=settings.working_dir,
        help="Working directory to work with log files",
    )
    mos_parser.add_argument(
        "--init-dir-path",
        default=settings.init_dir_path,
        help="Directory where files will be placed on <init> command",
    )
    mos_parser.add_argument(
        "--final-dir-path",
        default=settings.final_dir_path,
        help="Directory where files will be placed on <collect> command",
    )
    mos_parser.add_argument(
        "--stripped-dir-path",
        default=settings.stripped_dir_path,
        help="Directory where stripped log files will be placed for analysis",
    )
    mos_parser.add_argument(
        "--parse-input-dir-path",
        default=settings.parse_input_dir_path,
        help="Directory where all input log files will be placed",
    )
    mos_parser.add_argument(
        "--parse-output-dir-path",
        default=settings.parse_output_dir_path,
        help="Directory where all resulting output files will be placed",
    )
    mos_parser.add_argument(
        "--remote-collect-path",
        default=settings.remote_collect_path,
        help="Directory on remote host that will be downloaded for analysis",
    )
    mos_subparsers = mos_parser.add_subparsers(
        dest="module_cmd",
        help="Commands for MOS workflow")
    for func_name, func in [(key, value) for (key, value) in globals().items()
                            if callable(value) and key.startswith("do_")]:
        cmd_parser = mos_subparsers.add_parser(
            func_name[3:],
            help=func.__doc__ or '')
        cmd_parser.set_defaults(func=func)
        arguments = getattr(func, "arguments", [])
        for (args, kwargs) in arguments:
            cmd_parser.add_argument(*args, **kwargs)
