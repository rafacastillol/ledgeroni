from ledgeroni import parser
from collections import defaultdict
from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                             IgnoreSymbol, DefaultCommodity, Journal)


@dataclass
class Journal:
    transactions: List[Transaction] = field(default_factory=list)
    accounts: Set[Tuple[str]] = field(default_factory=set)
    commodities: Set[Commodity] = field(default_factory=set)
    prices: List[Price] = field(default_factory=list)
    default_commodity: Commodity = None
    ignored_symbols: List[str] = field(default_factory=list)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.accounts.update(p.account for p in transaction.postings)
        self.commodities.update(p.commodity for p in transaction.postings)


    @classmethod
    def build_journal_from_file(cls, filename, journal=None):
        if journal is None:
            journal = cls()

        for result in parser.read_file(filename):
            if isinstance(result, Transaction):
                journal.add_transaction(result)
            elif isinstance(result, DefaultCommodity):
                journal.default_commodity = result.commodity
            elif isinstance(result, IgnoreSymbol):
                journal.ignored_symbols.append(result.symbol)
            elif isinstance(result, Price):
                journal.prices.append(result)

        return journal

