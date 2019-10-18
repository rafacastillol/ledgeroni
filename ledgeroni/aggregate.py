import functools
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from collections import defaultdict, deque
from ledgeroni.types import Commodity


@dataclass
class AccountAggregate:
    own_balances: Dict = field(default_factory=lambda: defaultdict(Fraction))
    subaccounts: Dict = field(
        default_factory=lambda: defaultdict(AccountAggregate))
    aggregates: Dict = field(default_factory=lambda: defaultdict(Fraction))

    def add_commodity(self, account, amount, commodity):
        if len(account):
            self.aggregates[commodity] += amount
            self.subaccounts[account[0]].add_commodity(account[1:], amount,
                                                       commodity)
        else:
            self.own_balances[commodity] += amount
            self.aggregates[commodity] += amount

    def get_account_aggregates(self, account):
        if len(account) == 0:
            return self.aggregates
        return self.subaccounts[account[0]].get_account_aggregates(account[1:])


    def iter_aggregates(self):
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
                while len(agg.subaccounts) == 1:
                    # This will only iterate once lol
                    for n, c in agg.subaccounts.items():
                        name += ':' + n
                        agg = c
                stack.append((agg, level, name))

