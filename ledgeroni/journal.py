from ledgeroni import parser
from collections import defaultdict
from fractions import Fraction
from dataclasses import dataclass, field
from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                             IgnoreSymbol, DefaultCommodity)
from ledgeroni.query import Query
from typing import List, Set, Tuple, Dict
from ledgeroni.aggregate import AccountAggregate

@dataclass
class Journal:
    transactions: List[Transaction] = field(default_factory=list)
    accounts: Set[Tuple[str]] = field(default_factory=set)
    commodities: Set[Commodity] = field(default_factory=set)
    prices: List[Price] = field(default_factory=list)
    default_commodity: Commodity = None
    ignored_symbols: List[str] = field(default_factory=list)
    aggregate: AccountAggregate = None
    query: Query = None


    def add_transaction(self, transaction, calc_totals=True):
        """
        Adds and indexes a transaction.
        """
        if not self.query or transaction.matches_query(self.query):
            self.transactions.append(transaction)
            self.accounts.update(p.account for p in transaction.postings)
            self.commodities.update(c for p in transaction.postings
                                    if p.amounts for c in p.amounts)
            self.update_aggregate(transaction)

    def add_from_file(self, filename: str, calc_totals: bool=True):
        """
        Loads all objects from a journal file
        """
        for result in parser.read_file(filename):
            if isinstance(result, Transaction):
                self.add_transaction(result, calc_totals)
            elif isinstance(result, DefaultCommodity):
                self.default_commodity = result.commodity
            elif isinstance(result, IgnoreSymbol):
                self.ignored_symbols.append(result.symbol)
            elif isinstance(result, Price):
                self.prices.append(result)

    def update_aggregate(self, transaction: Transaction):
        """
        If the journal is keeping an aggregate, update it with the
        postings from the given transaction
        """
        if self.aggregate is None:
            return
        transaction = transaction.calc_totals()
        for posting in transaction.postings_matching(self.query):
            if posting.amounts is None:
                continue
            for c, a in posting.amounts.items():
                self.aggregate.add_commodity(posting.account, a, c)

