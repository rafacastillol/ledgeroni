import re
from datetime import datetime
import arrow
from ledgeroni.journal import Journal
from ledgeroni.query import And, Or, Not, RegexQuery, PayeeQuery
from ledgeroni.types import Transaction, Posting, Commodity

def test_add_transaction():
    journal = Journal()

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='Purchased reddit gold for the year')
    trans.add_posting(Posting(
        account=('Asset', 'Bitcoin Wallet'),
        amounts={None: -10.0}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))

    journal.add_transaction(trans)

    assert trans in journal.transactions


def test_add_transaction():
    journal = Journal()

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='Purchased reddit gold for the year')
    trans.add_posting(Posting(
        account=('Asset', 'Bitcoin Wallet'),
        amounts={None: -10.0}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))

    journal.add_transaction(trans)

    assert trans in journal.transactions


class TestTransactionsMatching:
    def test_filter_pass(self):
        journal = Journal()

        trans = Transaction(
            date=arrow.get(datetime(2013, 2, 20)),
            description='Purchased reddit gold for the year')
        trans.add_posting(Posting(
            account=('Asset', 'Bitcoin Wallet'),
            amounts={None: -10.0}))
        trans.add_posting(Posting(
            account=('Expense', 'Web Services', 'Reddit'),
            amounts=None))

        journal.add_transaction(trans)

        assert trans in journal.transactions_matching(
                query=RegexQuery(re.compile('Reddit')))


    def test_filter_pass(self):
        journal = Journal()

        trans = Transaction(
            date=arrow.get(datetime(2013, 2, 20)),
            description='Purchased reddit gold for the year')
        trans.add_posting(Posting(
            account=('Asset', 'Bitcoin Wallet'),
            amounts={None: -10.0}))
        trans.add_posting(Posting(
            account=('Expense', 'Web Services', 'Digg'),
            amounts=None))

        journal.add_transaction(trans)

        assert trans not in journal.transactions_matching(
                query=RegexQuery(re.compile('Reddit')))
