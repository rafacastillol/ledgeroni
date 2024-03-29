"""
journal.py: Defines an abstraction for a ledger journal and common operations
on them
"""
from collections import defaultdict
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Set, Tuple, Iterator, Dict
from ledgeroni import parser
from ledgeroni.types import (Transaction, Commodity, Price,
                             IgnoreSymbol, DefaultCommodity)
from ledgeroni.query import Query


@dataclass
class Journal:
    "Abstracts a ledger journal"
    transactions: List[Transaction] = field(default_factory=list)
    accounts: Set[Tuple[str]] = field(default_factory=set)
    commodities: Set[Commodity] = field(default_factory=set)
    prices: List[Price] = field(default_factory=list)
    default_commodity: Commodity = None
    ignored_symbols: List[str] = field(default_factory=list)

    def add_transaction(self, transaction: Transaction):
        "Adds and indexes a transaction."
        self.transactions.append(transaction)
        self.accounts.update(p.account for p in transaction.postings)
        self.commodities.update(c for p in transaction.postings
                                if p.amounts for c in p.amounts)

    def add_from_file(self, filename: str):
        "Loads all objects from a journal file"
        for result in parser.read_file(filename):
            if isinstance(result, Transaction):
                self.add_transaction(result)
            elif isinstance(result, DefaultCommodity):
                self.default_commodity = result.commodity
            elif isinstance(result, IgnoreSymbol):
                self.ignored_symbols.append(result.symbol)
            elif isinstance(result, Price):
                self.prices.append(result)

    def generate_running_total_report(
            self, query: Query) -> Iterator[Tuple[Transaction, Dict]]:
        """
        Generates a running total from the transactions stored in the journal.
        """
        totals = defaultdict(Fraction)

        for transaction in self.transactions:
            if not query.execute(transaction):
                continue
            transaction = transaction.calc_totals()
            trans_total = {}
            for posting in transaction.postings:
                for commodity, amount in posting.amounts.items():
                    totals[commodity] += amount
                posting_total = {c: a for c, a in totals.items() if a != 0}
                total = (posting.amounts, posting_total)
                trans_total[posting.account_name] = total
            yield transaction, trans_total

    def transactions_matching(self, query: Query) -> Iterator[Transaction]:
        "Returns this journals transactions filtered by a query"
        return (t for t in self.transactions if query.execute(t))

    def verify_transaction_balances(self) -> List[Transaction]:
        errors = []
        for transaction in self.transactions:
            if not transaction.verify_balance():
                errors.append(transaction)

        return errors
