"""
sorter.py: Sorting journals dynamically through user defined terms
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Iterable

from ledgeroni.journal import Journal
from ledgeroni.types import Transaction


@dataclass
class JournalSorter:
    "Class for sorting a journal's transactions according to a set of terms"
    trans_terms: List[Tuple[bool, str]] = field(default_factory=list)

    def process_term(self, term: str):
        "Processes a given term and adds it to the list"
        reverse = False
        if term[0] == '-':
            reverse = True
            term = term[1:]

        if term in ('d', 'date'):
            self.trans_terms.append((reverse, 'date'))

    @staticmethod
    def get_trans_term_key(term, trans: Transaction):
        "Builds a subkey for the given transaction and term"
        reverse, term = term
        if term == 'date':
            key = trans.date.timestamp
            if reverse:
                key = -key

        return key

    def build_transaction_key(self, transaction: Transaction) -> Tuple:
        "Builds a full key combining all the subkeys from transactions"
        key = tuple(self.get_trans_term_key(term, transaction)
                    for term in self.trans_terms)
        return key

    def sort_transactions(self, transactions: Iterable[Transaction]):
        "Sorts a list of transactions"
        transactions.sort(key=self.build_transaction_key)

    def sort_journal(self, journal: Journal):
        "Sorts a journal's transactions"
        self.sort_transactions(journal.transactions)

    @classmethod
    def from_term_list(cls, terms: Iterable[str]) -> JournalSorter:
        "Builds a sorter from a list of string terms"
        ins = cls()
        for term in terms:
            ins.process_term(term)
        return ins
