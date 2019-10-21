from datetime import datetime
import arrow

from ledgeroni.sorter import JournalSorter
from ledgeroni.types import Transaction

def test_from_term_list():
    terms = ['d']

    sorter = JournalSorter.from_term_list(terms)
    assert sorter.trans_terms == [(False, 'date')]

    terms = ['date']

    sorter = JournalSorter.from_term_list(terms)
    assert sorter.trans_terms == [(False, 'date')]

    terms = ['-d']

    sorter = JournalSorter.from_term_list(terms)
    assert sorter.trans_terms == [(True, 'date')]


def test_sort_transactions():
    trans1 = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='Purchased reddit gold for the year')

    trans2 = Transaction(
        date=arrow.get(datetime(2012, 2, 20)),
        description='Paid a parking ticket')

    trans3 = Transaction(
        date=arrow.get(datetime(2011, 2, 20)),
        description='Donated to charity')

    trans_list = [trans1, trans2, trans3]

    sorter = JournalSorter.from_term_list(('d',))
    sorter.sort_transactions(trans_list)

    assert trans_list == [trans3, trans2, trans1]

    trans_list = [trans2, trans1, trans3]

    sorter = JournalSorter.from_term_list(('-d',))
    sorter.sort_transactions(trans_list)

    assert trans_list == [trans1, trans2, trans3]
