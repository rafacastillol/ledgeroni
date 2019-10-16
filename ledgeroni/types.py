from arrow.arrow import Arrow
from dataclasses import dataclass, field
from typing import List

@dataclass
class Commodity:
    name: str
    is_prefix: bool = False

    @property
    def symbol(self):
        return self.name.strip()


@dataclass
class Posting:
    account: List[str]
    commodity: Commodity
    amount: float


@dataclass
class Transaction:
    date: Arrow
    description: str
    postings: List[Posting] = field(default_factory=list)

    def add_posting(self, posting):
        self.postings.append(posting)


@dataclass
class Price:
    timestamp: Arrow
    source: Commodity
    dest: Commodity
    rate: float


@dataclass
class IgnoreSymbol:
    symbol: str

@dataclass
class DefaultCommodity:
    commodity: Commodity
