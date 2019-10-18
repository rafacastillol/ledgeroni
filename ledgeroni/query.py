"""
query.py Abstraction for filtering account names
"""
import re
from dataclasses import dataclass
from typing import Tuple, Iterable


@dataclass(frozen=True)
class Query:
    "Base abstract query class"


@dataclass(frozen=True)
class RegexQuery(Query):
    "Query to match a datum to a regular expression"
    regex: re.Pattern

    def execute(self, data: str) -> bool:
        "Runs the query on `data`"
        return self.regex.match(data) is not None


@dataclass(frozen=True)
class Or(Query):
    "Query to combine multiple subqueries with an OR operation"
    queries: Tuple[Query]

    def execute(self, data: str) -> bool:
        "Runs the query on data"
        return any(q.execute(data) for q in self.queries)


def build_simple_or_query(strs: Iterable[str]) -> Query:
    "Builds an or query from an iterator of regular expressions"
    queries = tuple([RegexQuery(re.compile(s)) for s in strs])
    return Or(queries)
