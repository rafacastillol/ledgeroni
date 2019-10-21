from ledgeroni.query import And, Or, Not, RegexQuery
import re

def test_and():
    q = And((RegexQuery(re.compile('Expense')),
             RegexQuery(re.compile('Reddit'))))

    assert q.execute('Expense:Web Services:Reddit') == True

