"""
sorter.py: Sorting journals dynamically through user defined terms
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Iterable

from ledgeroni.journal import Journal
from ledgeroni.types import Transaction, Posting


@dataclass
class JournalSorter:
    "Class for sorting a journal's transactions according to a set of terms"
    trans_terms: List[Tuple[bool, str]] = field(default_factory=list)
    post_terms: List[Tuple[bool, str]] = field(default_factory=list)

    def process_term(self, term: str):
        "Processes a given term and adds it to the list"
        reverse = False
        if term[0] == '-':
            reverse = True
            term = term[1:]

        if term in ('d', 'date'):
            self.trans_terms.append((reverse, 'date'))
        if term in ('description', 'desc'):
            self.trans_terms.append((reverse, 'description'))
        if term in ('a', 'amount'):
            self.post_terms.append((reverse, 'amount'))

    @staticmethod
    def get_trans_term_key(term, trans: Transaction):
        "Builds a subkey for the given transaction and term"
        reverse, term = term
        if term == 'date':
            key = trans.date.timestamp
            if reverse:
                key = -key
        elif term == 'description':
            key = trans.description

        return key

    @staticmethod
    def get_post_term_key(term, post: Posting):
        "Builds a key for a posting and a specific term"
        reverse, term = term
        if term == 'amount':
            multi = -1 if reverse else 1
            amounts = []
            if post.amounts:
                for commodity, amount in post.amounts.items():
                    amounts.append((commodity.symbol, amount * multi))
            return tuple(amounts)

    def build_posting_key(self, post: Posting):
        "Builds a key for a posting"
        key = tuple(self.get_post_term_key(term, post)
                    for term in self.post_terms)
        return key

    def build_transaction_key(self, transaction: Transaction) -> Tuple:
        "Builds a full key combining all the subkeys from transactions"
        key = tuple(self.get_trans_term_key(term, transaction)
                    for term in self.trans_terms)
        return key

    def sort_transactions(self, transactions: Iterable[Transaction]):
        "Sorts a list of transactions"
        if self.trans_terms:
            transactions.sort(key=self.build_transaction_key)
        if self.post_terms:
            for transaction in transactions:
                transaction.postings.sort(key=self.build_posting_key)

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
