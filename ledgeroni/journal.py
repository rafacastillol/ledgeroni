from ledgeroni import parser
from collections import defaultdict
from fractions import Fraction
from dataclasses import dataclass, field
from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                             IgnoreSymbol, DefaultCommodity)
from ledgeroni.query import Query
from ledgeroni.sorter import JournalSorter
from typing import List, Set, Tuple, Dict, Iterator
from ledgeroni.aggregate import AccountAggregate
import copy

@dataclass
class Journal:
    transactions: List[Transaction] = field(default_factory=list)
    accounts: Set[Tuple[str]] = field(default_factory=set)
    commodities: Set[Commodity] = field(default_factory=set)
    prices: List[Price] = field(default_factory=list)
    default_commodity: Commodity = None
    ignored_symbols: List[str] = field(default_factory=list)
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

    def generate_running_total_report(self) -> Iterator:
        totals = defaultdict(Fraction)
        
        for transaction in self.transactions:
            transaction = transaction.calc_totals()
            trans_total = {}
            for posting in transaction.postings:
                for commodity, amount in posting.amounts.items():
                    totals[commodity] += amount
                posting_total = {c: a for c, a in totals.items() if a != 0}
                trans_total[posting.account_name] = posting.amounts, posting_total
            yield transaction, trans_total
