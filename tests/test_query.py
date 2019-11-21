from datetime import datetime
from fractions import Fraction
import arrow
from ledgeroni.query import And, Or, Not, RegexQuery, PayeeQuery
from ledgeroni.types import Transaction, Posting, Commodity
import re

USD = Commodity(is_prefix=True, name='$')

TRANS_1 = Transaction(
    date=arrow.get(datetime(2013, 2, 20)),
    description='Purchased reddit gold for the year')
TRANS_1.add_posting(Posting(
    account=('Asset', 'Bitcoin Wallet'),
    amounts={None: -10.0}))
TRANS_1.add_posting(Posting(
    account=('Expense', 'Web Services', 'Reddit'),
    amounts=None))


TRANS_2 = Transaction(
    date=arrow.get(datetime(2013, 2, 20)),
    description='Spent some cool cash')
TRANS_2.add_posting(Posting(
    account=('Bank', 'Paypal'),
    amounts={USD: -10.0}))
TRANS_2.add_posting(Posting(
    account=('Cool', 'Thing'),
    amounts=None))


TRANS_3 = Transaction(
    date=arrow.get(datetime(2013, 2, 20)),
    description='Purchased whatever digg sells for the year')
TRANS_3.add_posting(Posting(
    account=('Asset', 'Bitcoin Wallet'),
    amounts={None: -10.0}))
TRANS_3.add_posting(Posting(
    account=('Expense', 'Web Services', 'Digg'),
    amounts=None))


TRANS_4 = Transaction(
    date=arrow.get(datetime(2013, 2, 20)),
    description='I owe Joe a favor')
TRANS_4.add_posting(Posting(
    account=('Payable', 'Joe', 'Favor'),
    amounts={USD: -10.0}))
TRANS_4.add_posting(Posting(
    account=('Expense', 'Favor'),
    amounts=None))


TRANS_5 = Transaction(
    date=arrow.get(datetime(2013, 2, 20)),
    description='Traded some cards')
TRANS_5.add_posting(Posting(
    account=('Asset', 'Pokemon Cards'),
    amounts={None: -10.0}))
TRANS_5.add_posting(Posting(
    account=('Asset', 'MTG Cards'),
    amounts=None))


def test_regex_query():
    q = RegexQuery(re.compile('Expense'))

    print(q.execute(TRANS_1))
    assert q.execute(TRANS_1)
    assert not q.execute(TRANS_2)


def test_and():
    q = And((RegexQuery(re.compile('Expense')),
             RegexQuery(re.compile('Reddit'))))
    assert q.execute(TRANS_1)
    assert not q.execute(TRANS_3)


def test_or():
    q = Or((RegexQuery(re.compile('Digg')),
            RegexQuery(re.compile('Reddit'))))

    assert q.execute(TRANS_1)
    assert not q.execute(TRANS_2)
    assert q.execute(TRANS_3)


def test_not():
    q = Not(RegexQuery(re.compile('Asset')))

    assert q.execute(TRANS_1)
    assert not q.execute(TRANS_5)

def test_payee():
    q = PayeeQuery(RegexQuery(re.compile('reddit')))

    assert q.execute(TRANS_1)
    assert not q.execute(TRANS_2)
