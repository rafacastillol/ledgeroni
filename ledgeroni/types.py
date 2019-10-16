from arrow.arrow import Arrow
from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Set, Tuple, Dict

def recursive_default_dict():
    return defaultdict(recursive_default_dict)

@dataclass(frozen=True)
class Commodity:
    name: str
    is_prefix: bool = False

    @property
    def symbol(self):
        return self.name.strip()


@dataclass(frozen=True)
class Posting:
    account: Tuple[str]
    commodity: Commodity
    amount: float


@dataclass
class Transaction:
    date: Arrow
    description: str
    postings: List[Posting] = field(default_factory=list)

    def add_posting(self, posting):
        self.postings.append(posting)


@dataclass(frozen=True)
class Price:
    timestamp: Arrow
    source: Commodity
    dest: Commodity
    rate: float


@dataclass
class AccountAggregate:
    name: str
    own_balance: float = 0
    subaccounts: Dict = field(default_factory=dict)

    def compute_aggregate(self):
        return self.own_balance + sum(a.compute_aggregate() for a 
                                      in self.subaccounts.values())

    @classmethod
    def build_from_accounts(cls, accounts):
        root = recursive_default_dict()
        for account in accounts:
            current = root
            for lvl in account:
                current = current[lvl]

        return cls.build_from_dict_tree(None, root)

    @classmethod
    def build_from_dict_tree(cls, name, subtree):
        children = {key: cls.build_from_dict_tree(key, children)
                    for k, children in subtree.values()}

        return AccountAggregate(name=name, own_balance=0, subtree=children)



@dataclass(frozen=True)
class IgnoreSymbol:
    symbol: str


@dataclass(frozen=True)
class DefaultCommodity:
    commodity: Commodity


