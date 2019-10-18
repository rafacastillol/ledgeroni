import re
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class JournalSorter:
    trans_terms: List[Tuple[bool, str]] = field(default_factory=list)

    def process_term(self, term):
        reverse = False
        if term[0] == '-':
            reverse = True
            term = term[1:]

        if term == 'd' or term == 'date':
            self.trans_terms.append((reverse, 'date'))

    @staticmethod
    def get_trans_term_key(term, trans):
        reverse, term = term
        if term == 'date':
            key = trans.date.timestamp
            if reverse:
                key = -key

        return key

    def build_transaction_key(self, transaction):
        key = tuple(self.get_trans_term_key(term, transaction)
                     for term in self.trans_terms)
        return key

    def sort_transactions(self, transactions):
        transactions.sort(key=self.build_transaction_key)

    def sort_journal(self, journal):
        self.sort_transactions(journal.transactions)

    @classmethod
    def from_term_list(cls, terms):
        ins = cls()
        for term in terms:
            ins.process_term(term)
        return ins

        

