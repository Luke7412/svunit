from argparse import ArgumentParser
from pathlib import Path
from typing import List
from jinja2 import Template

from .model import TestSuite, TestRunner


################################################################################
def create_testrunner(output_file: Path, test_suites: List[TestSuite]):
    test_runner = TestRunner(output_file)

    # Check if all test suites exist
    for test_suite in test_suites:
        if not test_suite.path.exists():
            raise Exception(f'{test_suite.path} does not exist')

    print(f'SVUNIT: Creating testrunner {test_runner.class_name}:')

    template_path = Path(__file__).parent / 'templates/testrunner.jinja2'
    template = Template(template_path.read_text())

    rendering = template.render(
        test_runner=test_runner,
        test_suites=test_suites
    )

    output_file.write_text(rendering)


################################################################################
def parse_args():
    parser = ArgumentParser(description='Create Testrunner Script')
    parser.add_argument('--out', metavar='<file>', dest='output_file', required=True, type=lambda p: Path(p))
    parser.add_argument('--add', metavar='<filename>', dest='files_to_add', nargs='+', required=True, type=lambda p: Path(p))
    parser.add_argument('--overwrite', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    create_testrunner(
        output_file=args.output_file,
        files_to_add=[TestSuite(x) for x in args.files_to_add]
    )
