import subprocess
from argparse import ArgumentParser
from pathlib import Path

from .build_svunit import build_svunit
from .utils import get_test_suites, remove_tree
from . import __version__


################################################################################
def validate_args(args):
    if not args.defines:
        args.defines = list()


def clean(path: Path):
    files = [
        path / 'run.log',
        path / '.svunit.f',
        path / 'vsim.wlf',
        path / 'ncsc.log',
        path / 'irun.key',
        *get_test_suites(path)
    ]
    dirs = [
        path / 'INCA_libs'
    ]

    for file in files:
        if file.exists():
            file.unlink()

    for path in dirs:
        if path.exists():
            remove_tree(path)


def get_version(args):
    version = __version__
    args.defines.append(f'SVUNIT_VERSION="{version.strip()}"')


def get_commands(args):

    # Load required generator
    if args.simulator in ['modelsim', 'riviera']:
        from .simulators.modelsim import generate_commands
    elif args.simulator == "vcs":
        from .simulators.vcs import generate_commands
    elif args.simulator in ['questa','ius', 'xcelium']:
        from .simulators.xcelium import generate_commands
    else:
        raise Exception('Simulator not supported')

    return generate_commands(args)


def run_svunit(args):
    print(args)

    validate_args(args)
    clean(args.output_dir)
    get_version(args)

    commands = get_commands(args)

    # Build SVUnit
    build_svunit(
        output_dir=args.output_dir,
        tests=args.tests,
        mock=args.uvm,
        uvm=args.uvm,
        wavedrom=args.wavedrom,
    )

    for command in commands:
        print(command)

    for command in commands:
        subprocess.run(command, cwd=args.output_dir)


###############################################################################
def parse_args():
    parser = ArgumentParser(description='Create Unit Test Script')

    parser.add_argument(
        '-s', '--sim', metavar='<simulator>', dest='simulator', required=True,
        type=str, choices=['questa', 'modelsim', 'riviera', 'ius', 'xcelium', 'vcs'],
        help='simulator is either of questa, modelsim, riviera, ius, xcelium, vcs or dsim'
    )
    parser.add_argument(
        '-l', '--log', metavar='<log>', dest='logfile', type=lambda p: Path(p),
        default=Path('run.log'), help='simulation log file (default: run.log)'
    )
    parser.add_argument(
        '-d', '--define', metavar='<macro>', dest='defines', nargs='+',
        help='appended to the command line as +define+<macro>'
    )
    parser.add_argument(
        '-f', '--filelist', metavar='<file>', dest='filelists', nargs='+',
        default=[], type=lambda p: Path(p).absolute(),
        help='some verilog file list'
    )
    parser.add_argument(
        '-r', '--r_args', metavar='<option>', dest='simargs',
        type=lambda x: x.strip().split(), default=[],
        help='specify additional runtime options'
    )
    parser.add_argument(
        '-c', '--c_args', metavar='<option>', dest='compileargs',
        type=lambda x: x.strip().split(), default=[],
        help='specify additional compile options'
    )
    parser.add_argument(
        '-u', '--uvm', action='store_true', help='run SVUnit with UVM'
    )
    parser.add_argument(
        '-o', '--out', dest='output_dir', type=lambda p: Path(p).absolute(),
        default=Path.cwd(), help=' output directory for tmp and simulation files'
    )
    parser.add_argument(
        '-t', '--test', type=list, dest='tests', default=[],
        help='specifies a unit test to run (multiple can be given)'
    )
    parser.add_argument(
        '-m', '--mixedsim', metavar='<vhdlfile>', dest='vhdl_file',
        help='consolidated file list with VHDL files and command line switches'
    )
    parser.add_argument(
        '-w', '--wavedrom', action='store_true',
        help='process json files as wavedrom output'
    )
    parser.add_argument(
        '--filter', type=str, default='*',
        help='specify which tests to run, as <test_module>.<test_name>'
    )

    return parser.parse_args()


###############################################################################
def main():
    args = parse_args()
    run_svunit(args)


if __name__ == '__main__':
    main()
