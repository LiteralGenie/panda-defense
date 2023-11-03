from itertools import chain
from typing import Any, Literal, Type


class _EmptyList:
    pass


class WhereBuilder:
    mode: Literal["AND", "OR"]
    builders: "list[WhereBuilder]"
    conditions: list[str]
    values: list[list[Any]]

    def __init__(self):
        self.mode = "AND"
        self.builders = []
        self.conditions = []
        self.values = []

    def add(
        self,
        condition: str,
        values: list[Any] | Type[_EmptyList] = _EmptyList,
    ) -> None:
        if values is _EmptyList:
            values = []

        self.conditions.append(condition)
        self.values.append(values)

    def add_builder(self, wb: "WhereBuilder") -> None:
        self.builders.append(wb)

    def print(self, with_where: bool = True) -> tuple[str, list[Any]]:
        conds = self.conditions
        conds.extend(f"({b.print(with_where=False)})" for b in self.builders)

        clause = "WHERE " if with_where else ""
        clause += f" {self.mode} ".join(conds)

        values = list(chain(*self.values))

        return (clause, values)
