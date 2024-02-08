from dataclasses import dataclass
from pathlib import Path


################################################################################
@dataclass
class Base:
    rpl_str = ''
    rpl_with = ''

    path: Path

    @property
    def class_name(self):
        return self.path.stem

    @property
    def instance_name(self):
        return self.class_name.replace(self.rpl_str, self.rpl_with)


@dataclass
class TestRunner(Base):
    rpl_str = ''
    rpl_with = ''


@dataclass
class TestSuite(Base):
    rpl_str = '_testsuite'
    rpl_with = '_ts'


@dataclass
class UnitTest(Base):
    rpl_str = '_unit_test'
    rpl_with = '_ut'


@dataclass
class TypeTest(Base):
    rpl_str = '_type_test'
    rpl_with = '_tt'

