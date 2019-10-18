import re
from dataclasses import dataclass, field
from typing import Tuple, Iterable


@dataclass(frozen=True)
class Query:
    "Base abstract query class"
    pass


@dataclass(frozen=True)
class RegexQuery(Query):
    "Query to match a datum to a regular expression"
    regex: re.Pattern

    def execute(self, data: str) -> bool:
        return self.regex.match(data) is not None


@dataclass(frozen=True)
class Or(Query):
    "Query to combine multiple subqueries with an OR operation"
    qs: Tuple[Query]

    def execute(self, data: str) -> bool:
        return any(q.execute(data) for q in self.qs)


def build_simple_or_query(strs: Iterable[str]) -> Query:
    qs = tuple([RegexQuery(re.compile(s)) for s in strs])
    return Or(qs)
