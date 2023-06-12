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

    def __eq__(self: "Todo", obj: object) -> bool:
        """Compare by custom id."""
        if not isinstance(obj, Todo):
            return NotImplemented
        return self.id_ == obj.id_

    @property
    def place(self: "Todo") -> int:
        """Return the placement of self in calendar right now."""
        for num, todo in self.calendar.todos_of_month:
            if self == todo:
                return num
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
        for day in self.dates_of_month:
            for todo in self.day_todos(day):
                yield todo_n, todo
                todo_n += 1

    def day_todos(self: "Calendar", day: date) -> list[Todo]:
        """Return the todos of the date `day`."""
        return self.todos[str(day)]

    def preview_day_todos(self: "Calendar", day: date) -> str:
        """Return a comma-seperated string of all the date's todos."""
        return ", ".join(str(todo.place) for todo in self.day_todos(day))

    def add_todo(self: "Calendar", todo: Todo) -> Todo:
        """Add a todo to the calendar while setting self as the todo's calendar."""
        todo.calendar = self
        self.day_todos(todo.date).append(todo)
        return todo

    def remove_todo(self: "Calendar", todo_n: int) -> Todo | None:
        """
        Remove a todo from the calendar.

        Algorithm explanation: assuming the following:
            nested_list = [
                [a, b, c],
                [d, e, f, g, h],
                [X, j]
            ],

            target = #8, X (nexted_list[2][0]),
        then the algorithm goes like this:

        | n | target | sublist         | length | target in range? | new target | got |
        -------------------------------------------------------------------------------
        | 0 | 8      | [a, b, c]       | 3      | no (8 >= 3)      | 8 - 3 = 5  | N/A |
        | 1 | 5      | [d, e, f, g, h] | 5      | no (5 >= 5)      | 5 - 5 = 5  | N/A |
        | 2 | 0      | [X, j]          | 2      | yes (0 < 2)      | N/A        | 2,0 |
        """
        target = todo_n - 1
        for day in self.dates_of_month:
            day_todos = self.day_todos(day)
            day_len = len(day_todos)
            if target >= day_len:  # not in this day
                target -= day_len  # decrease and try again
            else:  # in this day
                return day_todos.pop(target)  # pop it
        return None

    def update_todo(self: "Calendar", todo: Todo) -> Todo:
        """Remove a todo and re-add it."""
        self.remove_todo(todo.place)
        self.add_todo(todo)
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
