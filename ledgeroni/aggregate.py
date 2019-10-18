"""
aggregate.py: tool for building aggregates over accounts in dynamically
"""
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Dict, Tuple
from collections import defaultdict, deque
from ledgeroni.types import Commodity


@dataclass
class AccountAggregate:
    "Builds a tree to calculate account and subaccount aggregates on the fly."
    own_balances: Dict = field(default_factory=lambda: defaultdict(Fraction))
    subaccounts: Dict = field(
        default_factory=lambda: defaultdict(AccountAggregate))
    aggregates: Dict = field(default_factory=lambda: defaultdict(Fraction))

    def add_commodity(self, account: Tuple[str], amount: Fraction,
                      commodity: Commodity):
        """
        Updates given account and parent accounts with the given amount  of
        commodity
        """
        if account:
            self.aggregates[commodity] += amount
            self.subaccounts[account[0]].add_commodity(account[1:], amount,
                                                       commodity)
        else:
            self.own_balances[commodity] += amount
            self.aggregates[commodity] += amount

    def add_transaction(self, transaction, query=None):
        "Adds a given transactions postings to the aggregate"
        transaction = transaction.calc_totals()
        for posting in transaction.postings_matching(query):
            if posting.amounts is None:
                continue
            for commodity, amount in posting.amounts.items():
                self.add_commodity(posting.account, amount, commodity)

    def add_from_journal(self, journal):
        "Adds all transactions in a journal to the aggregate"
        for transaction in journal.transactions:
            self.add_transaction(transaction, journal.query)

    def iter_aggregates(self):
        """Iterates through all aggregates in a depth first search, yielding
        visited accounts in a preorder fashion.
        """
        stack = deque([(self, 0, '')])
        while stack:
            agg, level, name = stack.pop()
            if level == 0 or len(agg.subaccounts) != 1:
                yield level, name, agg.aggregates
                child_keys = list(agg.subaccounts.keys())
                child_keys.sort(reverse=True)
                for child_key in child_keys:
                    child = agg.subaccounts[child_key]
                    stack.append((child, level + 1, child_key))
            else:
                # If node only has one child, combine it with it's child
                while len(agg.subaccounts) == 1:
                    # This will only iterate once lol
                    for child_name, child in agg.subaccounts.items():
                        name += ':' + child_name
                        agg = child
                stack.append((agg, level, name))
