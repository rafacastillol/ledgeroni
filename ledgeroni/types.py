"""
types.py: defines data types that are parsed from a ledger journal file
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Tuple, Dict, Iterator
import copy
from fractions import Fraction
from arrow.arrow import Arrow


@dataclass(frozen=True)
class Commodity:
    "Represents a type of commodity to be exchanged"
    name: str
    is_prefix: bool = False

    @property
    def symbol(self) -> str:
        "The commodity symbol without surrounding whitespace"
        return self.name.strip()

    def format_amount(self, amt: Fraction) -> str:
        "Formats the amount passed in with the commodity symbol"
        amt = '{:.2f}'.format(float(amt))
        if self.is_prefix:
            return self.name + amt
        return amt + self.name


class IntegerCommodity():
    name: str = ''
    is_prefix: bool = False

    @property
    def symbol(self) -> str:
        return ''

    def format_amount(self, amt: Fraction) -> str:
        "Formats the amount passed in with the commodity symbol"
        return '{:.2f}'.format(float(amt))


INTEGER_COMMODITY = IntegerCommodity()


@dataclass(frozen=True)
class Posting:
    "Represents a movement in a specific account"
    account: Tuple[str]
    amounts: Dict = field(default_factory=dict)

    @property
    def account_name(self) -> str:
        "Full account name as shown in the original posting"
        return ':'.join(self.account)

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

    @property
    def date_str(self):
        "Date of the transaction in journal format"
        return self.date.format('YYYY/MM/DD')

    @property
    def header(self):
        "The transaction header in journal format"
        return '{} {}'.format(self.date_str, self.description)

    def as_journal_format(self) -> str:
        "Returns the transaction formatted in a ledger journal format"
        return '\n'.join([self.header] + [p.as_journal_format()
                                          for p in self.postings])

    def verify_balance(self) -> bool:
        totals = defaultdict(Fraction)
        for posting in self.postings:
            # If a null amount posting exists, we're done
            if posting.amounts is None:
                return True
            for commodity, amount in posting.amounts.items():
                totals[commodity] += amount

        if len(totals) == 2:
            # Can auto balance if we have exactly two commodities
            return True

        return all(a == 0 for a in totals.values())

    def calc_totals(self) -> Transaction:
        """
        Returns a new transaction where postings with implicit amounts are
        made explicit
        """
        auto_posting = None
        totals = defaultdict(Fraction)
        for i, posting in enumerate(self.postings):
            if posting.amounts is None:
                if auto_posting is not None:
                    raise ValueError
                auto_posting = i
            else:
                for commodity, amount in posting.amounts.items():
                    totals[commodity] -= amount

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
    "Represents a historical price"
    timestamp: Arrow
    source: Commodity
    dest: Commodity
    rate: float


@dataclass(frozen=True)
class IgnoreSymbol:
    "Represents a symbol to be ignored in price definitions"
    symbol: str


@dataclass(frozen=True)
class DefaultCommodity:
    "Specifies a commodity to be used as default"
    commodity: Commodity


