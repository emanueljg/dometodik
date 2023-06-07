"""A module containing the calendar and TODOs"""

from dataclasses import dataclass, field
from datetime import date
from collections import defaultdict
from typing import Iterator, ClassVar


@dataclass
class Todo:
    _counter: ClassVar[int] = 0
    _id: int = field(init=False)

    date: date
    text: str
    calendar: "Calendar" = field(init=False)

    def __post_init__(self) -> None:
        self._id = Todo._counter
        Todo._counter += 1

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Todo):
            return NotImplemented
        return self._id == o._id

    @property
    def place(self) -> int:
        for n, todo in self.calendar.todos_of_month:
            if self == todo:
                return n
        raise ValueError


@dataclass
class Calendar:
    current_date: date
    todos: dict[str, list[Todo]] = field(default_factory=lambda: defaultdict(list))

    @property
    def day_is_max(self) -> bool:
        try:
            self.current_date.replace(day=self.current_date.day + 1)
        except ValueError:
            return True
        return False

    @property
    def dates_of_month(self) -> Iterator[date]:
        for day in range(1, 32):
            try:  # ask for forgiveness when going 1 day above month max
                yield date(
                    year=self.current_date.year, month=self.current_date.month, day=day
                )
            except ValueError:
                return

    @property
    def todos_of_month(self) -> Iterator[tuple[int, Todo]]:
        todo_n = 1
        for d in self.dates_of_month:
            for todo in self.day_todos(d):
                yield todo_n, todo
                todo_n += 1

    def day_todos(self, date: date) -> list[Todo]:
        return self.todos[str(date)]

    def preview_day_todos(self, date: date) -> str:
        return ", ".join(str(todo.place) for todo in self.day_todos(date))

    def add_todo(self, todo: Todo) -> Todo:
        todo.calendar = self
        self.day_todos(todo.date).append(todo)
        return todo
