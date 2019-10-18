import unittest
from ledgeroni import parser
from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                                   IgnoreSymbol, DefaultCommodity)
import arrow
from datetime import datetime
from fractions import Fraction

USD = Commodity(is_prefix=True, name='$')
AU = Commodity(is_prefix=False, name='AU')
BTC = Commodity(is_prefix=False, name=' BTC')

class TestParserMethods(unittest.TestCase):
    def test_remove_comments(self):
        res = list(parser.remove_comments(
            ('ok ; what', '# no way', 'no comment')))
        self.assertEqual(res, ['ok', '', 'no comment'])

    def test_remove_empty_lines(self):
        res = list(parser.remove_empty_lines(('line', '', 'lines')))
        self.assertEqual(res, ['line', 'lines'])

    def test_read_transaction_line(self):
        transaction = parser.read_transaction_line(
                '2013/2/20 Purchased reddit gold for the year')
        self.assertEqual(transaction, Transaction(
            date=arrow.get(datetime(2013, 2, 20)),
            description='Purchased reddit gold for the year'))

    def test_read_posting_line(self):
        posting_line = '	Asset:Bitcoin Wallet		-10'
        posting = Posting(
            account=('Asset', 'Bitcoin Wallet'),
            amounts={None: -10.0})
        result = parser.read_posting_line(posting_line)
        self.assertEqual(result, posting)

        posting_line = '	Payable:Joe:Favor	-$10'
        posting = Posting(
            account=('Payable', 'Joe', 'Favor'),
            amounts={USD: -10.0})
        result = parser.read_posting_line(posting_line)
        self.assertEqual(result, posting)

        posting_line = '	Payable:Joe:Favor	-10 BTC'
        posting = Posting(
            account=('Payable', 'Joe', 'Favor'),
            amounts={BTC: -10.0})
        result = parser.read_posting_line(posting_line)
        self.assertEqual(result, posting)

    def test_read_transactions(self):
        lines = ['2013/2/20 Purchased reddit gold for the year',
                 '	Asset:Bitcoin Wallet		-10',
                 '	Expense:Web Services:Reddit']
        result = list(parser.read_lines(lines))

        trans = Transaction(
            date=arrow.get(datetime(2013, 2, 20)),
            description='Purchased reddit gold for the year')
        trans.add_posting(Posting(
            account=('Asset', 'Bitcoin Wallet'),
            amounts={None: -10.0}))
        trans.add_posting(Posting(
            account=('Expense', 'Web Services', 'Reddit'),
            amounts=None))

        self.assertEqual(result[0], trans)

    def test_read_price_line(self):
        price_line = 'P 2012/11/25 05:04:00 AU $1751.90'
        price = Price(timestamp=arrow.get(datetime(2012, 11, 25, 5, 4, 0)),
                      source=AU,dest=USD, rate=Fraction('1751.90'))
        result = parser.read_price_line(price_line)

        self.assertEqual(result, price)

    def test_read_ignore_symbol_line(self):
        ignore_symbol_line = 'N $'
        ignore_symbol = IgnoreSymbol(USD.symbol)
        result = parser.read_ignore_symbol_line(ignore_symbol_line)
        self.assertEqual(result, ignore_symbol)

    def test_read_default_commodity_line(self):
        default_commodity_line = 'D $1,000.00'
        default_commodity = DefaultCommodity(USD)
        result = parser.read_default_commodity_line(default_commodity_line)
        self.assertEqual(result, default_commodity)
