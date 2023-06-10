"""A module containing the calendar and TODOs."""

from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import ClassVar


@dataclass
class Todo:
    """A class representing a calendar todo."""

    counter: ClassVar[int] = 0
    id_: int = field(init=False)

    date: date
    text: str
    calendar: "Calendar" = field(init=False)

    def __post_init__(self: "Todo") -> None:
        """Set the object ID with a class counter."""
        self.id_ = Todo.counter
        Todo.counter += 1

    def __eq__(self: "Todo", o: object) -> bool:
        """Compare by custom id."""
        if not isinstance(o, Todo):
            return NotImplemented
        return self.id_ == o.id_

    @property
    def place(self: "Todo") -> int:
        """Return the placement of self in calendar right now."""
        for n, todo in self.calendar.todos_of_month:
            if self == todo:
                return n
        raise ValueError


@dataclass
class Calendar:
    """A class representing a Calendar."""

    current_date: date
    todos: dict[str, list[Todo]] = field(default_factory=lambda: defaultdict(list))

    @property
    def dates_of_month(self: "Calendar") -> Iterator[date]:
        """Return all valid days in current month."""
        for day in range(1, 32):
            try:  # ask for forgiveness when going 1 day above month max
                yield date(
                    year=self.current_date.year,
                    month=self.current_date.month,
                    day=day,
                )
            except ValueError:
                return

    @property
    def todos_of_month(self: "Calendar") -> Iterator[tuple[int, Todo]]:
        """Aggregate all todos of all days of the current month."""
        todo_n = 1
        for d in self.dates_of_month:
            for todo in self.day_todos(d):
                yield todo_n, todo
                todo_n += 1

    def day_todos(self: "Calendar", date: date) -> list[Todo]:
        """Return the todos of the date `date`."""
        return self.todos[str(date)]

    def preview_day_todos(self: "Calendar", date: date) -> str:
        """Return a comma-seperated string of all the date's todos."""
        return ", ".join(str(todo.place) for todo in self.day_todos(date))

    def add_todo(self: "Calendar", todo: Todo) -> Todo:
        """Add a todo to the calendar while setting self as the todo's calendar."""
        todo.calendar = self
        self.day_todos(todo.date).append(todo)
        return todo

    @staticmethod
    def get_time() -> str:
        """Get today's time in `HH:MM` format."""
        return str(datetime.now(tz=timezone.utc).strftime("%H:%M"))

    @staticmethod
    def get_weekday() -> str:
        """Get today's weekday in long format `Friday`."""
        return str(datetime.now(tz=timezone.utc).strftime("%A"))

    @staticmethod
    def get_date() -> str:
        """Get today's date it short ISO (`yyyy-mm-dd`)."""
        return str(datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"))
