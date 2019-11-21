"""
query.py Abstraction for filtering account names
"""
import re
from dataclasses import dataclass
from typing import Tuple, Iterable, Set, Iterator

from ledgeroni.types import Transaction, Posting

@dataclass(frozen=True)
class Query:
    "Base abstract query class"

    def execute(self, trans: Transaction) -> Set[Posting]:
        raise NotImplementedError

    def postings_matching(self, trans: Transaction) -> Iterator[Posting]:
        return (trans.postings[i] for i in self.execute(trans))


@dataclass(frozen=True)
class RegexQuery(Query):
    "Query to match a datum to a regular expression"
    regex: re.Pattern

    def execute(self, trans: Transaction) -> Set[Posting]:
        "Runs the query on `data`"
        return {i for i, posting in enumerate(trans.postings)
                if self.regex.search(posting.account_name) is not None}


@dataclass(frozen=True)
class Or(Query):
    "Query to combine multiple subqueries with an OR operation"
    queries: Tuple[Query]

    def execute(self, trans: Transaction) -> Set[Posting]:
        "Runs the query on data"
        return set.union(*(q.execute(trans) for q in self.queries))


@dataclass(frozen=True)
class And(Query):
    "Query to combine multiple subqueries with an AND operation"
    queries: Tuple[Query]

    def execute(self, trans: Transaction) -> Set[Posting]:
        "Runs the query on data"
        return set.intersection(*(q.execute(trans) for q in self.queries))


@dataclass(frozen=True)
class Not(Query):
    "Query that wraps a query and returns the opposite result"
    query: Query

    def execute(self, trans: Transaction) -> Set[Posting]:
        "Runs the query on data"
        return set(range(len(trans.postings))) - self.query.execute(trans)


@dataclass(frozen=True)
class PayeeQuery(Query):
    """
    A query that matches a regex against the payee instead of the account names
    """
    query: RegexQuery

    def execute(self, trans: Transaction) -> Set[Posting]:
        "Runs the query on data"
        regex = self.query.regex
        if regex.search(trans.description) is None:
            return set([])
        return set(range(len(trans.postings)))


@dataclass(frozen=True)
class AlwaysTrueQuery(Query):
    "A query that always returns all elements"
    def execute(self, trans: Transaction):
        return set(range(len(trans.postings)))


MATCH_ALL = AlwaysTrueQuery()


def build_simple_or_query(strs: Iterable[str]) -> Query:
    "Builds an or query from an iterator of regular expressions"
    queries = tuple([RegexQuery(re.compile(s)) for s in strs])
    return Or(queries)
