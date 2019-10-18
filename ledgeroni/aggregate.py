import functools
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Set
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
        if len(account):
            self.aggregates[commodity] += amount
            self.subaccounts[account[0]].add_commodity(account[1:], amount,
                                                       commodity)
        else:
            self.own_balances[commodity] += amount
            self.aggregates[commodity] += amount

    def add_transaction(self, transaction, query=None):
        transaction = transaction.calc_totals()
        for posting in transaction.postings_matching(query):
            if posting.amounts is None:
                continue
            for c, a in posting.amounts.items():
                self.add_commodity(posting.account, a, c)

    def add_from_journal(self, journal):
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
                child_keys = [k for k in agg.subaccounts]
                child_keys.sort()
                for n in child_keys[::-1]:
                    c = agg.subaccounts[n]
                    stack.append((c, level + 1, n))
            else:
                # If node only has one child, combine it with it's child
                while len(agg.subaccounts) == 1:
                    # This will only iterate once lol
                    for n, c in agg.subaccounts.items():
                        name += ':' + n
                        agg = c
                stack.append((agg, level, name))

