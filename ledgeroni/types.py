import functools
from arrow.arrow import Arrow
from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Set, Tuple, Dict


@dataclass(frozen=True)
class Commodity:
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
    account: Tuple[str]
    amounts: Dict = field(default_factory=dict)

    @property
    def account_name(self):
        return ':'.join(self.account)

    def matches_query(self, query):
        return query.execute(self.account_name)

    def as_journal_format(self):
        amount_str = ''
        if self.amounts:
            amount_str = ' '.join(c.format_amount(a)
                                  for c, a in self.amounts.items())
        return '\t{:<25}\t{:>20}'.format(self.account_name, amount_str)


@dataclass
class Transaction:
    date: Arrow
    description: str
    postings: List[Posting] = field(default_factory=list)

    def add_posting(self, posting):
        self.postings.append(posting)

    def matches_query(self, query):
        return any(p.matches_query(query) for p in self.postings)

    def postings_matching(self, query):
        if query is None:
            return self.postings
        else:
            return (p for p in self.postings if p.matches_query(query))

    def as_journal_format(self):
        date_str = self.date.format('YYYY/MM/DD')
        header = '{} {}'.format(date_str, self.description)
        return '\n'.join([header] + [p.as_journal_format()
                                     for p in self.postings])



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


