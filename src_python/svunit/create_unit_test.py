from argparse import ArgumentParser
from pathlib import Path
from jinja2 import Template
from enum import Enum, auto


class ProcessingType (Enum):
    CLASS = auto()
    MODULE = auto()
    INTERFACE = auto()


################################################################################
def create_unit_test(args):

    print(f'SVUNIT: Creating unit_test:')

    template_path = Path(__file__).parent / 'templates/unit_test.jinja2'
    template = Template(template_path.read_text())

    if args.class_name:
        uut = args.class_name
    elif args.module_name:
        uut = args.module_name
    elif args.if_name:
        uut = args.if_name

    rendering = template.render(
        uut=uut,
        uvm_test=args.uvm,
    )

    output_file = Path(f'{uut}_unit_test.sv')
    output_file.write_text(rendering)


################################################################################
def parse_args():
    parser = ArgumentParser(description='Create Unit Test Script')
    parser.add_argument('--uvm', action='store_true', help='generate a uvm component test template. IMPORTANT: do not use "-uvm" unless the UUT is derived from a uvm_component')
    parser.add_argument('--out', metavar='<file>', dest='output_file', type=lambda p: Path(p), help='specifies a new default output file')
    parser.add_argument('--overwrite', action='store_true', help='overwrites the output file if it already exists')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--class_name', metavar='<name>', type=str, help='generate a unit test template for a class <name>')
    group.add_argument('--module_name', metavar='<name>', type=str, help='generate a unit test template for a module <name>')
    group.add_argument('--if_name', metavar='<name>', type=str, help='generate a unit test template for an interface <name>')
    group.add_argument('--file', metavar='uut.sv', type=lambda p: Path(p), help='the file with the unit under test')
    return parser.parse_args()


def validate_args(args):
    if not args.file and not args.class_name and not args.module_name and not args.if_name:
        raise Exception('The testfile was either not specified, does not exist or is not readable')

    else:
        if not args.output_file.endswith('_unit_test.sv'):
            raise Exception('The testfile was either not specified, does not exist or is not readable')


################################################################################
def main():
    args = parse_args()
    validate_args(args)
    create_unit_test(args)


if __name__ == '__main__':
    main()
