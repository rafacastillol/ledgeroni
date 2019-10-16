import unittest
import ledgeroni.parser as parser
from ledgeroni.transaction import Transaction
import arrow
from datetime import datetime

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

