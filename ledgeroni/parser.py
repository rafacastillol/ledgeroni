"""
parser.py: parses a rudimentary verison of the ledger journal format

Details on the file format were lifted from the official documentation,
(https://www.ledger-cli.org/3.0/doc/ledger3.html#Journal-Format), however,
some features of the file were left out for simplicity's sake. Some of these
ommisions include:

* The only command directives that are accepted are `include`, `P`, `D`, `N`
* Marking transactions as clear or pending has no effect.
* Can't specify cost with @ syntax


"""
import re
import itertools
import os
import arrow
from typing import Iterator

from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                             IgnoreSymbol, DefaultCommodity)


def load_lines(filename: str) -> Iterator[str]:
    """
    Returns an iterator of lines from the contents of `filename`. This will
    also follow any `include` directives specified in the file and iterate
    over those too
    """
    cwd = os.path.dirname(filename)
    with open(filename) as fp:
        for line in fp:
            if line.startswith('!include') or line.startswith('include'):
                for f in line.split()[1:]:
                    p = f if os.path.isabs(f) else os.path.join(cwd, f)
                    yield from load_lines(p)
            else:
                yield line


def remove_comments(it: Iterator[str]) -> Iterator[str]:
    "Removes comments that start with [;#%*] from `it`"
    return (re.sub('[;#%|*].*$', '', line).rstrip() for line in it)


def remove_empty_lines(it: Iterator[str]) -> Iterator[str]:
    "Filters `it` for lines that have no content"
    return (line for line in it if line)


def read_transaction_line(l: str) -> str:
    """
    Reads the line that begins a transaction and returns a new transaction 
    object
    """
    date, description = l.split(maxsplit=1)
    date = arrow.get(date)
    return Transaction(date=date, description=description)
    

def read_posting_line(l: str) -> Posting:
    "Reads a posting line and returns a Posting object"
    l = l.strip()

    # The account name ends once we find two spaces in a row
    account, amount = l, None
    for i, c in enumerate(l[:-2]):
        if c.isspace() and l[i+1].isspace() or c == '\t':
            account, amount = l[0:i].strip(), l[i:].strip()
            break


    account = tuple(account.split(':'))
    amount, commodity = read_amount(amount)

    return Posting(account=account, commodity=commodity, amount=amount)


amount_re = re.compile(
    r'(?P<negation>-?)(?P<prefix>[^.,\d-]*)(?P<amount>[.,\d]+)'
    r'(?P<suffix>[^.,\d-]*)')


def read_amount(s):
    """
    Reads in a journal formatted amount and returns the numerical amount
    along with an associated commodity object
    """
    if s is None:
        return None, None

    m = amount_re.match(s.strip())
    prefix = m.group('prefix')
    amount = m.group('amount').replace(',', '')
    suffix = m.group('suffix')
    negation = m.group('negation')

    # Can't have both prefix and suffix
    if prefix and suffix:
        raise ValueError

    multi = -1 if negation else 1
    amount = float(amount)
    commodity = None
    if prefix:
        commodity = Commodity(is_prefix=True, name=prefix)
    if suffix:
        commodity = Commodity(is_prefix=False, name=suffix)
    return amount * multi, commodity


def read_price_line(l):
    """
    Reads a line that specifies a historical price in journal format and
    returns a Price object
    """
    parts = l.split(maxsplit=4)
    
    _, date, time, source, amount = parts

    src = Commodity(name=source)
    rate, dest = read_amount(amount)

    dt = arrow.get(date + ' ' + time)

    return Price(timestamp=dt, source=src, dest=dest, rate=rate)


def read_ignore_symbol_line(l):
    _, symbol = l.split(maxsplit=1)
    return IgnoreSymbol(symbol=symbol)


def read_default_commodity_line(l):
    _, amount = l.split(maxsplit=1)
    _, commodity = read_amount(amount)
    return DefaultCommodity(commodity)


def read_lines(it):
    current_transaction = None
    for line in it:
        if line[0].isspace():
            if not current_transaction:
                raise ValueError
            current_transaction.add_posting(read_posting_line(line))
            continue
        if current_transaction is not None:
            yield current_transaction
        if line[0].isdigit():
            current_transaction = read_transaction_line(line)
        elif line[0] == 'P':
            yield read_price_line(line)
        elif line[0] == 'N':
            yield read_ignore_symbol_line(line)
        elif line[0] == 'D':
            yield read_default_commodity_line(line)
        else:
            raise ValueError

    if current_transaction is not None:
        yield current_transaction


def read_file(filename: str):
    it = load_lines(filename)
    it = remove_comments(it)
    it = remove_empty_lines(it)
    yield from read_lines(it)

