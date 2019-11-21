from datetime import datetime
import pytest
import arrow
from ledgeroni.types import Transaction, Posting, Commodity

USD = Commodity(is_prefix=True, name='$')

def example_transactions():
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

    return [TRANS_1, TRANS_2, TRANS_3, TRANS_4, TRANS_5]

