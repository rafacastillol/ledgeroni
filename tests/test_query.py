from ledgeroni.query import And, Or, Not, RegexQuery
import re


def test_regex_query():
    q = RegexQuery(re.compile('Expense'))

    assert q.execute('Expense:Web Services:Reddit') == True
    assert q.execute('Something:Expense:Web Services:Reddit') == True


def test_and():
    q = And((RegexQuery(re.compile('Expense')),
             RegexQuery(re.compile('Reddit'))))

    assert q.execute('Expense:Web Services:Reddit') == True
    assert q.execute('Expense:Food') == False
    assert q.execute('We:Did:It:Reddit') == False
    assert q.execute('Bank:Paypal') == False


def test_or():
    q = Or((RegexQuery(re.compile('Expense')),
             RegexQuery(re.compile('Reddit'))))

    assert q.execute('Expense:Web Services:Reddit') == True
    assert q.execute('Expense:Food') == True
    assert q.execute('We:Did:It:Reddit') == True
    assert q.execute('Bank:Paypal') == False


def test_not():
    q = Not(RegexQuery(re.compile('Expense')))

    assert q.execute('Expense:Web Services:Reddit') == False
    assert q.execute('Bank:Paypal') == True
