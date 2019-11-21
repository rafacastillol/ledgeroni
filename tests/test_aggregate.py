from datetime import datetime
import re
from fractions import Fraction
import arrow
from ledgeroni.aggregate import AccountAggregate
from ledgeroni.types import Commodity, Transaction, Posting
from ledgeroni.query import RegexQuery, Not
from ledgeroni.journal import Journal

USD = Commodity(is_prefix=True, name='$')
AU = Commodity(is_prefix=False, name='AU')
BTC = Commodity(is_prefix=False, name=' BTC')

def test_add_commodity():
    agg = AccountAggregate()
    agg.add_commodity(('Bank', 'Paypal'), Fraction (10, 1), USD)
    agg.add_commodity(('Bank', 'Banorte'), Fraction (20, 1), USD)
    agg.add_commodity(('Asset', 'Bitcoin'), Fraction (2, 1), BTC)

    assert agg.aggregates == {USD: 30, BTC: 2}

def test_add_transaction():
    agg = AccountAggregate()

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='Purchased reddit gold for the year')
    trans.add_posting(Posting(
        account=('Asset', 'Bitcoin Wallet'),
        amounts={BTC: -10}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))

    agg.add_transaction(trans)

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='2012/7/1 Partial payment from Client X')
    trans.add_posting(Posting(
        account=('Bank', 'Paypal'),
        amounts={USD: 350}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))

    agg.add_transaction(trans)

    assert agg.aggregates == {USD: 0, BTC: 0}


def test_query_filtering():
    agg = AccountAggregate(query=Not(RegexQuery(re.compile('Asset'))))

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='Purchased reddit gold for the year')
    trans.add_posting(Posting(
        account=('Asset', 'Bitcoin Wallet'),
        amounts={BTC: -10}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))

    agg.add_transaction(trans)

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='2012/7/1 Partial payment from Client X')
    trans.add_posting(Posting(
        account=('Bank', 'Paypal'),
        amounts={USD: 350}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))

    agg.add_transaction(trans)

    assert agg.aggregates == {USD: 0, BTC: Fraction(10)}


def test_add_from_journal():
    agg = AccountAggregate()
    journal = Journal()

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='Purchased reddit gold for the year')
    trans.add_posting(Posting(
        account=('Asset', 'Bitcoin Wallet'),
        amounts={BTC: -10}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))
    journal.add_transaction(trans)

    trans = Transaction(
        date=arrow.get(datetime(2013, 2, 20)),
        description='2012/7/1 Partial payment from Client X')
    trans.add_posting(Posting(
        account=('Bank', 'Paypal'),
        amounts={USD: 350}))
    trans.add_posting(Posting(
        account=('Expense', 'Web Services', 'Reddit'),
        amounts=None))
    journal.add_transaction(trans)

    agg.add_from_journal(journal)

    assert agg.aggregates == {USD: 0, BTC: 0}
