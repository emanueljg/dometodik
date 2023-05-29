from pytest import fixture, raises
from typing import Any, NoReturn
from collections.abc import Iterator, Iterable

from ..helpers import elems_with_attrs


class C:
    def __init__(self, x: Any = None, y: Any = None, z: Any = None) -> None:
        self.x = x
        self.y = y
        self.z = z

@fixture
def empty_iterator() -> Iterator[None]:
    return iter([])

@fixture
def empty_list() -> list[None]:
    return []

@fixture
def iterable_of_c() -> Iterable[C]:
    return (c for c in (
        C(x='x'), C(x='x', y='y'), C(x='x', y='y', z='z')
    ))

@fixture
def list_of_c(iterable_of_c: Iterable[C]) -> list[C]:
    return list(iterable_of_c)

def test_empty_iter_elems_with_attrs(empty_list: list[None]) -> None:
    platter = elems_with_attrs(empty_list, walk='silly')
    assert next(platter, 'tipped over') == 'tipped over'

def test_empty_list_elems_with_attrs(empty_iterator: Iterator[None]) -> None:
    got = elems_with_attrs(empty_iterator, parrot='polly')
    assert next(got, 'stone dead') == 'stone dead'

def test_invalid_elems_with_attrs(list_of_c: list[C]) -> None:
    die = elems_with_attrs(list_of_c, weapon='banana')
    with raises(AttributeError):
        next(die)

def test_open_elems_with_attrs(list_of_c: list[C]) -> None:
    spam = elems_with_attrs(list_of_c)
    assert list(spam) == list_of_c 

def test_many_elems_with_attrs(list_of_c: list[C]) -> None:    
    yes = C(x='x', y='y')
    no = C(x='x')
    input = [yes, no, yes]
    got = elems_with_attrs(input, x='x', y='y')
    assert list(got) == [yes, yes]
 
