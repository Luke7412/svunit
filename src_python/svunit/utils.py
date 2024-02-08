from pathlib import Path
from typing import List, Callable


################################################################################
def walk(path: Path):
    for p in path.iterdir():
        if p.is_dir():
            yield from walk(p)
            continue
        yield p.resolve()


def remove_tree(path: Path):
    for child in path.glob('*'):
        if child.is_dir():
            remove_tree(child)
        else:
            child.unlink()
    path.rmdir()


################################################################################
def get_files(path: Path, match: Callable[[Path], bool]) -> List[Path]:
    if not path.exists():
        return []

    return [p for p in walk(path) if p.is_file() and match(p)]


def get_test_suites(path: Path) -> List[Path]:
    return get_files(path, lambda x: x.name.endswith('_testsuite.sv'))


def get_unit_tests(path: Path) -> List[Path]:
    return get_files(path, lambda x: x.name.endswith('_unit_test.sv'))
