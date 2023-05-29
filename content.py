"""A module containing the content class and its instances"""

__all__ = ['Content']

from dataclasses import dataclass
from typing import ClassVar, Hashable, Any
from flask_login import current_user

# written this way to avoid circular import
from . import helpers


Contents = dict[str, 'Content']
@dataclass
class Content:
    name: str
    has_text: bool = True
    protected: bool = False
    is_login: bool = False

    ALL: ClassVar[Contents] = {}

    def __post_init__(self) -> None:
        self.ALL[self.name] = self

    @property
    def capitalized(self) -> str:
        return self.name[0].upper() + self.name[1:]

    @property
    def html(self) -> str:
        return self.name + '.html'

    def _css_classify(self, stub: str, selected_content: 'Content') -> str:
        return stub if self != selected_content else stub + ' selected'

    def css_classify_button(self, selected_content: 'Content') -> str:
        return self._css_classify('contentButton', selected_content)

    def css_classify_content(self, selected_content: 'Content') -> str:
        return self._css_classify('content', selected_content)
       
    @classmethod
    def with_attrs(cls, **attrs: Any) -> Contents:
        # somewhat annoying tweaks to make mypy happy
        elems = helpers.elems_with_attrs(cls.ALL, **attrs)
        return {str(k): v for (k, v) in elems}

    @classmethod
    def HAS_TEXT(cls) -> Contents:
        return cls.with_attrs(has_text=True)

    @classmethod
    def UNPROTECTEDS(cls) -> Contents:
        return cls.with_attrs(protected=False)

    @classmethod
    def ALL_EXCEPT_LOGIN(cls) -> Contents:
        new_dict = cls.ALL.copy()
        del new_dict['login']
        return new_dict

    @classmethod
    def contextual_contents(cls) -> Contents:
        return cls.ALL_EXCEPT_LOGIN() \
                if current_user.is_authenticated \
            else cls.UNPROTECTEDS()
    

# is automatically added to Content.ALL, just type them here
Content('login')
Content('logout', has_text=False, protected=True)
Content('home')
Content('members')

