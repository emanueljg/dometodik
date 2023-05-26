"""A module containing helper functions."""

__all__ = ['elems_with_attrs', 'base_render']

from flask import render_template
from collections.abc import Iterable, Iterator, Mapping

from .content import Content


def _obj_has_attrs(o, **attrs) -> bool:
    """Check if an object has the specified attributes

    :param o: The object to check
    :param **attrs: The attributes' keys and values to check

    :return: True if object has the specified attributes, False otherwise
    """
    return all(getattr(o, k) == v for k, v in attrs.items())

def elems_with_attrs(iterable: Iterable|Mapping, **attrs) \
    -> Iterator|Iterator[tuple]:
    """Get elements of an `Iterable` with the specified attributes

    The return type differs based on the type of the collection:
    - A subtype of `Mapping` in turn returns an `Iterator` of tuples
      representing key-value pairs in which the 'value' object has
      the specified attributes.
    - A subtype of `Iterable` **which isn't a `Mapping`** returns an `Iterator` of
      elements with the same type as the elements of the `Iterable`.

    :param itr: The `Iterable` to filter
    :param attrs: Kwargs of attributes to filter the `Iterable` with 

    :return: An `Iterator` of elements
    """
    if isinstance(iterable, Mapping):
        iterable = iterable.items()
        def __obj_has_attrs(o, **attrs):
            return _obj_has_attrs(o[1], **attrs)
    else: __obj_has_attrs = _obj_has_attrs
    tmp = (o for o in iterable if __obj_has_attrs(o, **attrs))
    return tmp

def base_render(content: str = 'home', failed_login: bool = False):
    return render_template('base.html', 
                           selected_content=Content.ALL[content],
                           Content=Content,
                           failed_login=failed_login)

