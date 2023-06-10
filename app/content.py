"""A module containing the content class and its instances."""

__all__ = ["Content"]

from dataclasses import dataclass
from typing import Any, ClassVar

from flask_login import current_user

# written this way to avoid circular import
from . import helpers

Contents = dict[str, "Content"]


@dataclass
class Content:
    """A class representing content of a page."""

    name: str
    has_text: bool = True
    protected: bool = False
    is_login: bool = False

    ALL: ClassVar[Contents] = {}

    def __post_init__(self: "Content") -> None:
        """Add self to class object registry."""
        self.ALL[self.name] = self

    @property
    def capitalized(self: "Content") -> str:
        """Return content name in all caps."""
        return self.name[0].upper() + self.name[1:]

    @property
    def html(self: "Content") -> str:
        """Return the template file name."""
        return self.name + ".html"

    def _css_classify(self: "Content", stub: str, selected_content: "Content") -> str:
        """Return the contextual CSS class(es) of self."""
        return stub if self != selected_content else stub + " selected"

    def css_classify_button(self: "Content", selected_content: "Content") -> str:
        """Target content buttons with CSS classification."""
        return self._css_classify("contentButton", selected_content)

    def css_classify_content(self: "Content", selected_content: "Content") -> str:
        """Target main content with CSS classification."""
        return self._css_classify("content", selected_content)

    @classmethod
    def with_attrs(cls: type["Content"], **attrs: Any) -> Contents:  # noqa: ANN401
        """Return all the elements that have attributes equal said values."""
        elems = helpers.elems_with_attrs(cls.ALL, **attrs)
        return {str(k): v for (k, v) in elems}

    @classmethod
    def with_text(cls: type["Content"]) -> Contents:
        """Return all contents that semantically 'contain text'."""
        return cls.with_attrs(has_text=True)

    @classmethod
    def unprotecteds(cls: type["Content"]) -> Contents:
        """Return all contents that don't require login to access."""
        return cls.with_attrs(protected=False)

    @classmethod
    def all_except_login(cls: type["Content"]) -> Contents:
        """Return all contents except for the `login` content."""
        new_dict = cls.ALL.copy()
        del new_dict["login"]
        return new_dict

    @classmethod
    def contextual_contents(cls: type["Content"]) -> Contents:
        """Return content based on if we are logged in or not."""
        return (
            cls.all_except_login()
            if current_user.is_authenticated
            else cls.unprotecteds()
        )


# is automatically added to Content.ALL, just type them here
Content("login")
Content("logout", has_text=False, protected=True)
Content("home")
Content("members")
Content("calendar", protected=True)
