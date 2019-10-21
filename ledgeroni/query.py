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
        return self.regex.search(data) is not None


@dataclass(frozen=True)
class Or(Query):
    "Query to combine multiple subqueries with an OR operation"
    queries: Tuple[Query]

    def execute(self, data: str) -> bool:
        "Runs the query on data"
        return any(q.execute(data) for q in self.queries)

@dataclass(frozen=True)
class And(Query):
    "Query to combine multiple subqueries with an AND operation"
    queries: Tuple[Query]

    def execute(self, data: str) -> bool:
        "Runs the query on data"
        return all(q.execute(data) for q in self.queries)

@dataclass(frozen=True)
class Not(Query):
    "Query that wraps a query and returns the opposite result"
    query: Query

    def execute(self, data: str) -> bool:
        "Runs the query on data"
        return not self.query.execute(data)


def build_simple_or_query(strs: Iterable[str]) -> Query:
    "Builds an or query from an iterator of regular expressions"
    queries = tuple([RegexQuery(re.compile(s)) for s in strs])
    return Or(queries)
