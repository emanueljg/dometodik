"""Test the helpers."""
from collections.abc import Iterable, Iterator

import pytest

from dometodik.helpers import elems_with_attrs

# many functions are self-explanatory, cba
# ruff: noqa: D103

# pylint: disable=invalid-name, missing-function-docstring, redefined-outer-name


class C:
    """Dummy class containing some attributes."""

    # pylint: disable=too-few-public-methods

    def __init__(
        self: "C",
        x: str | None = None,
        y: str | None = None,
        z: str | None = None,
    ) -> None:
        """Init values."""
        self.x = x
        self.y = y
        self.z = z


@pytest.fixture()
def empty_iterator() -> Iterator[None]:
    return iter([])


@pytest.fixture()
def empty_list() -> list[None]:
    return []


@pytest.fixture()
def iterable_of_c() -> Iterable[C]:
    return (c for c in (C(x="x"), C(x="x", y="y"), C(x="x", y="y", z="z")))


@pytest.fixture()
def list_of_c(iterable_of_c: Iterable[C]) -> list[C]:
    return list(iterable_of_c)


def test_empty_iter_elems_with_attrs(empty_list: list[None]) -> None:
    platter = elems_with_attrs(empty_list, walk="silly")
    assert next(platter, "tipped over") == "tipped over"


def test_empty_list_elems_with_attrs(empty_iterator: Iterator[None]) -> None:
    got = elems_with_attrs(empty_iterator, parrot="polly")
    assert next(got, "stone dead") == "stone dead"


def test_invalid_elems_with_attrs(list_of_c: list[C]) -> None:
    die = elems_with_attrs(list_of_c, weapon="banana")
    with pytest.raises(AttributeError):
        next(die)


def test_open_elems_with_attrs(list_of_c: list[C]) -> None:
    spam = elems_with_attrs(list_of_c)
    assert list(spam) == list_of_c


def test_many_elems_with_attrs() -> None:
    yes = C(x="x", y="y")
    no = C(x="x")
    input_ = [yes, no, yes]
    got = elems_with_attrs(input_, x="x", y="y")
    assert list(got) == [yes, yes]
