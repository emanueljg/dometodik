"""A module containing helper functions."""

__all__ = ["elems_with_attrs", "base_render"]

from flask import render_template
from collections.abc import Iterable, Iterator, Mapping, Hashable
from typing import Any, Optional
from datetime import date


from . import content
from .calendar import Calendar


def _obj_has_attrs(o: Any, **attrs: Any) -> bool:
    """Check if an object has the specified attributes

    :param o: The object to check
    :param **attrs: The attributes' keys and values to check

    :return: True if object has the specified attributes, False otherwise
    """
    return all(getattr(o, k) == v for k, v in attrs.items())


def elems_with_attrs(
    iterable: Iterable[Any] | Mapping[Hashable, Any], **attrs: Any
) -> Iterator[Any] | Iterator[tuple[Hashable, Any]]:
    """Get elements of an `Iterable` with the specified attributes

    The return type differs based on the type of the collection:
    - A subtype of `Mapping` in turn returns an `Iterator` of
      tuples representing key-value pairs in which the 'value'
      object has the specified attributes.
    - A subtype of `Iterable` **which isn't a `Mapping`** returns an
      `Iterator` of elements with the same type as the elements of the
      `Iterable`.

    :param itr: The `Iterable` to filter
    :param attrs: Kwargs of attributes to filter the `Iterable` with

    :return: An `Iterator` of elements
    """
    if isinstance(iterable, Mapping):
        iterable = iterable.items()

        def __obj_has_attrs(o: Any, **attrs: Any) -> bool:
            return _obj_has_attrs(o[1], **attrs)

    else:
        __obj_has_attrs = _obj_has_attrs
    return (o for o in iterable if __obj_has_attrs(o, **attrs))


def base_render(
    route: str = "home", failed_login: bool = False, calendar: Optional[Calendar] = None
) -> str:
    """Render base HTML with custom Jinja variables

    This facilitates things like displaying the selected content based
    on the content route and peripheral things like styling the selected
    content button.

    The flow for, say, the Home content can be roughly written as:
        1. Navigate to /home
        2. This function gets called with the route '/home'
        3. Resolve this route to a Content object
            * i.e. `Content.ALL['home']` => Content('home', has_text=true, ...)
        4. Send the content object as well as some other info as Jinja vars.
        5. Through templating create the site HTML and CSS based on the object
            * Set the "Home" button as active
            * Set the home.html as displayed

    :param route: The currently selected route, evaluates to `Content`
    :param failed_login: Whether the last login attempt failed or not

    :return: The rendered HTML
    """
    return render_template(
        "base.html",
        selected_content=content.Content.ALL[route],
        Content=content.Content,
        failed_login=failed_login,
        calendar=calendar or Calendar(date(year=1970, month=1, day=1)),
    )
