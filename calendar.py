"""A module containing the calendar and TODOs"""

from dataclasses import dataclass, field
from datetime import date
from collections import defaultdict


@dataclass
class Todo:
    date: date
    text: str


@dataclass
class Calendar:
    todos: dict[str, list[Todo]] = field(default_factory=lambda: defaultdict(list))

    def todos_of_month(self, grep: date) -> list[Todo]:
        month = []
        for day in range(1, 32):
            try:  # ask for forgiveness when going 1 day above month max
                date_key = str(date(year=grep.year, month=grep.month, day=day))
            except ValueError:
                break
            month.append(self.todos[str(date_key)])
        return month

    def add_todo(self, todo: Todo):
        self.todos[str(todo.date)].append(todo)


cal1 = Calendar()
bday = cal1.todos_of_month(grep=date(year=2023, month=5, day=1))
print(len(bday))
