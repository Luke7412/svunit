import os
from pathlib import Path
from argparse import ArgumentParser
from typing import List

from . import utils
from .create_testrunner import create_testrunner
from .create_testsuite import create_testsuite
from .model import UnitTest, TestSuite
from .utils import get_files, get_test_suites


################################################################################
def get_svunit_dot_f_files(path: Path):
    return get_files(path, lambda x: x.name == 'svunit.f')


################################################################################
def build_test_runner(output_dir: Path):
    create_testrunner(
        output_file=output_dir / 'testrunner.sv',
        test_suites=[TestSuite(p) for p in get_test_suites(Path.cwd())],
    )
    return (output_dir / 'testrunner.sv').as_posix()


################################################################################
def build_test_suite(path: Path, output_dir: Path, tests: List[Path]) -> str:
    unit_tests = get_unit_tests(path, tests)

    # replace ./- characters with _
    txt = ''

    # create the testsuite for this directory
    if unit_tests:
        create_testsuite(
            output_file=output_dir / f'{path.stem}_testsuite.sv',
            files_to_add=unit_tests,
            overwrite=True
        )

        txt += f'+incdir+{output_dir.as_posix()}\n'
        txt += f'{(output_dir / (path.stem + "_testsuite.sv")).as_posix()}\n'

        for unit_test in unit_tests:
            txt += f'{unit_test.path.as_posix()}\n'

    # recursively do the same through sub-directories
    if not tests:
        for p in path.iterdir():
            if p.is_dir():
                txt += build_test_suite(p, output_dir, tests)

    return txt


def get_unit_tests(path: Path, tests: List[Path]):
    unit_tests = []
    if tests:
        for test in tests:
            test_path = path / test
            if test_path.exists():
                unit_tests.append(test_path)
            else:
                raise Exception(f'Unit test {test} could not be found in directory {path}')
    else:
        unit_tests = utils.get_unit_tests(path)

    return [UnitTest(path) for path in unit_tests]


################################################################################
def build_svunit(output_dir: Path, tests: List[Path], mock: bool, uvm: bool, wavedrom: bool):
    output_dir.mkdir(parents=True, exist_ok=True)

    svunit_base = Path(__file__).parent.resolve() / 'svunit_base'
    cwd = Path.cwd()

    dot_svunit_dot_f_file = output_dir / '.svunit.f'
    txt = ''
    txt += f'+incdir+{cwd.as_posix()}\n'
    txt += f'+incdir+{(svunit_base / "junit-xml").as_posix()}\n'
    txt += f'{(svunit_base / "junit-xml/junit_xml.sv").as_posix()}\n'
    txt += f'+incdir+{(svunit_base / "").as_posix()}\n'
    txt += f'{(svunit_base / "svunit_pkg.sv").as_posix()}\n'
    if mock:
        txt += f'{(svunit_base / "uvm-mock/svunit_uvm_mock_pkg.sv").as_posix()}\n'
    if uvm:
        txt += f'+incdir+{(svunit_base / "uvm-mock").as_posix()}\n'
        txt += f'{(svunit_base / "uvm-mock/svunit_uvm_mock_pkg.sv").as_posix()}\n'

    if wavedrom:
        pass
        # system(f'python3 {svunit_install}/bin/wavedromSVUnit.py')

    files = get_svunit_dot_f_files(cwd)      # ??
    for file in files:
        txt += f'-f {file}\n'

    txt += build_test_suite(cwd, output_dir, tests)
    txt += build_test_runner(output_dir)

    dot_svunit_dot_f_file.write_text(txt)


################################################################################
def parse_args():
    parser = ArgumentParser(description='Build SVUnit Script')
    parser.add_argument('-o', '--out', metavar='<dir>', dest='output_dir', type=lambda p: Path(p), default=Path.cwd(), help='output directory for tmp and simulation files')
    parser.add_argument('-t', '--test', metavar='<test>', dest='tests', type=str, help='specifies a unit test to run (multiple can be given)')
    parser.add_argument('-m', '--mock', action='store_true', help='includes the uvm_mock_pkg to the final build file')
    parser.add_argument('-u', '--uvm', action='store_true', help='build SVUnit with UVM')
    parser.add_argument('-w', '--wavedrom', action='store_true', help='process json files as wavedrom output')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    build_svunit(
        output_dir=args.output_dir,
        tests=args.tests,
        mock=args.mock,
        uvm=args.uvm,
        wavedrom=args.wavedrom
    )
