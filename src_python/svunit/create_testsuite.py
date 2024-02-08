import argparse
from pathlib import Path
from typing import List, Union
from jinja2 import Template

from .model import UnitTest, TestSuite


################################################################################
def create_testsuite(output_file: Path, files_to_add: List[Union[UnitTest, TestSuite]], overwrite: bool):
    test_suite = TestSuite(output_file)

    # unit_tests = get_unit_tests(files_to_add)
    # unit_tests = [UnitTest(x) for x in unit_tests]

    # type_tests = []
    # for to_add in files_to_add:
    #     type_tests.append(TypeTest(to_add))

    print(f'SVUNIT: Creating class {test_suite.class_name}:')

    template_path = Path(__file__).parent / 'templates/testsuite.jinja2'
    template = Template(template_path.read_text())

    rendering = template.render(
        test_suite=test_suite,
        unit_tests=files_to_add
    )

    output_file.write_text(rendering)


################################################################################
def parse_args():
    parser = argparse.ArgumentParser(description='Create Testrunner Script')
    parser.add_argument(
        '-out', 
        metavar='<file>', 
        dest='files_to_add', 
        required=True, 
        type=lambda p: Path(p),
        help='specifies an output filename'
    )
    parser.add_argument(
        '-add', 
        metavar='<filename>', 
        dest='files_to_add', 
        nargs='+', 
        required=True, 
        type=lambda p: Path(p),
        help='adds test to test suite'
    )
    parser.add_argument(
        '-overwrite', 
        action='store_true',
        help='overwrites the output file if it already exists'
    )
    return parser.parse_args()


def validate_args(args):
    if not args.overwrite and args.output_file.exists():
        raise Exception('ERROR: The file already exists, to overwrite, use the -overwrite argument')


if __name__ == '__main__':
    args = parse_args()
    validate_args(args)

    create_testsuite(
        output_file=args.output_file,
        files_to_add=args.files_to_add,
        overwrite=args.overwrite
    )
