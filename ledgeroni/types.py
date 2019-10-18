from __future__ import annotations
import functools
import copy
from fractions import Fraction
from arrow.arrow import Arrow
from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Set, Tuple, Dict, Iterator
from ledgeroni.query import Query


@dataclass(frozen=True)
class Commodity:
    "Represents a type of commodity to be exchanged"
    name: str
    is_prefix: bool = False

    @property
    def symbol(self):
        return self.name.strip()

    def format_amount(self, amt):
        amt = '{:.2f}'.format(float(amt))
        if self.is_prefix:
            return self.name + amt
        else:
            return amt + self.name


@dataclass(frozen=True)
class Posting:
    "Represents a movement in a specific account"
    account: Tuple[str]
    amounts: Dict = field(default_factory=dict)

    @property
    def account_name(self) -> str:
        "Full account name as shown in the original posting"
        return ':'.join(self.account)

    def matches_query(self, query: Query) -> bool:
        "Returns whether the posting matches the given query"
        return query.execute(self.account_name)

    def as_journal_format(self) -> str:
        "Returns the posting formatted in a ledger journal format"
        amount_str = ''
        if self.amounts:
            amount_str = ' '.join(c.format_amount(a)
                                  for c, a in self.amounts.items())
        return '\t{:<25}\t{:>20}'.format(self.account_name, amount_str)


@dataclass
class Transaction:
    "Represents a transaction of commodities"
    date: Arrow
    description: str
    postings: List[Posting] = field(default_factory=list)

    def add_posting(self, posting: Posting):
        "Adds a posting to this transaction"
        self.postings.append(posting)

    def matches_query(self, query: Query) -> bool:
        "Returns a boolean that indicates if any of the postings match the query"
        return any(p.matches_query(query) for p in self.postings)

    def postings_matching(self, query) -> Iterator:
        "Returns an iterator of postings that match query"
        if query is None:
            return self.postings
        else:
            return (p for p in self.postings if p.matches_query(query))

    def as_journal_format(self) -> str:
        "Returns the transaction formatted in a ledger journal format"
        date_str = self.date.format('YYYY/MM/DD')
        header = '{} {}'.format(date_str, self.description)
        return '\n'.join([header] + [p.as_journal_format()
                                     for p in self.postings])

    def calc_totals(self) -> Transaction:
        """
        Returns a new transaction where postings with implicit amounts are
        made explicit
        """
        auto_posting = None
        totals = defaultdict(Fraction)
        for i, p in enumerate(self.postings):
            if p.amounts is None:
                if auto_posting is not None:
                    raise ValueError
                auto_posting = i
            else:
                for c, a in p.amounts.items():
                    totals[c] -= a

        new_trans = self
        if auto_posting is not None:
            new_trans = copy.copy(self)
            new_trans.postings = new_trans.postings[:]
            new_trans.postings[auto_posting] = Posting(
                account=self.postings[auto_posting].account,
                amounts=totals)
        return new_trans





@dataclass(frozen=True)
class Price:
    timestamp: Arrow
    source: Commodity
    dest: Commodity
    rate: float


@dataclass(frozen=True)
class IgnoreSymbol:
    symbol: str


@dataclass(frozen=True)
class DefaultCommodity:
    commodity: Commodity


