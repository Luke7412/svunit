from pathlib import Path
from typing import List

from .utils import walk, remove_tree, get_test_suites, get_unit_tests


################################################################################
def get_generated_files(path: Path) -> List[Path]:
    files = []
    for file in walk(path):
        if file.name.endswith('testsuite.sv') or file.name.endswith('testrunner.sv'):
            files.append(file)
    return files


def clean(path: Path):
    files = [
        path / 'run.log',
        path / 'compile.log',
        path / '.svunit.f',
        path / 'vsim.wlf',
        path / 'ncsc.log',
        path / 'irun.key',
        path / 'simv',
        *get_test_suites(path),
        *get_unit_tests(path)
    ]

    dirs = [
        path / 'INCA_libs',
        path / 'csrc',
        path / 'simv.daidir'
    ]

    for file in files:
        if file.exists():
            file.unlink()

    for path in dirs:
        if path.exists():
            remove_tree(path)


###############################################################################
if __name__ == '__main__':
    clean(Path(__file__).parent)
