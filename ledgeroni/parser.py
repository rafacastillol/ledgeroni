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
from typing import Iterator, Tuple
from fractions import Fraction
import re
import os
import arrow

from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                             IgnoreSymbol, DefaultCommodity)


def load_lines(filename: str) -> Iterator[str]:
    """
    Returns an iterator of lines from the contents of `filename`. This will
    also follow any `include` directives specified in the file and iterate
    over those too
    """
    cwd = os.path.dirname(filename)
    with open(filename) as filep:
        for line in filep:
            if line.startswith('!include') or line.startswith('include'):
                for new_filename in line.split()[1:]:
                    filepath = (new_filename if os.path.isabs(new_filename)
                                else os.path.join(cwd, new_filename))
                    yield from load_lines(filepath)
            else:
                yield line


def remove_comments(iterator: Iterator[str]) -> Iterator[str]:
    "Removes comments that start with [;#%*] from `it`"
    return (re.sub('[;#%|*].*$', '', line).rstrip() for line in iterator)


def remove_empty_lines(iterator: Iterator[str]) -> Iterator[str]:
    "Filters `it` for lines that have no content"
    return (line for line in iterator if line)


def read_transaction_line(line: str) -> str:
    """
    Reads the line that begins a transaction and returns a new transaction
    object
    """
    date, description = line.split(maxsplit=1)
    date = arrow.get(date)
    return Transaction(date=date, description=description)


def read_posting_line(line: str) -> Posting:
    "Reads a posting line and returns a Posting object"
    line = line.strip()

    # The account name ends once we find two spaces in a row
    account, amount = line, None
    for i, next_char in enumerate(line[:-2]):
        if next_char.isspace() and line[i+1].isspace() or next_char == '\t':
            account, amount = line[0:i].strip(), line[i:].strip()
            break

    account = tuple(account.split(':'))
    amount, commodity = read_amount(amount)
    amounts = None if amount is None else {commodity: amount}

    return Posting(account=account, amounts=amounts)


AMOUNT_RE = re.compile(
    r'(?P<negation>-?)(?P<prefix>[^.,\d-]*)(?P<amount>[.,\d]+)'
    r'(?P<suffix>[^.,\d-]*)')


def read_amount(amtstr: str) -> Tuple[Fraction, Commodity]:
    """
    Reads in a journal formatted amount and returns the numerical amount
    along with an associated commodity object
    """
    if amtstr is None:
        return None, None

    match = AMOUNT_RE.match(amtstr.strip())
    prefix = match.group('prefix')
    amount = match.group('amount').replace(',', '')
    suffix = match.group('suffix')
    negation = match.group('negation')

    # Can't have both prefix and suffix
    if prefix and suffix:
        raise ValueError

    multi = -1 if negation else 1
    amount = Fraction(amount)
    commodity = None
    if prefix:
        commodity = Commodity(is_prefix=True, name=prefix)
    if suffix:
        commodity = Commodity(is_prefix=False, name=suffix)
    return amount * multi, commodity


def read_price_line(line: str) -> Price:
    """
    Reads a line that specifies a historical price in journal format and
    returns a Price object
    """
    parts = line.split(maxsplit=4)

    _, date, time, source, amount = parts

    src = Commodity(name=source)
    rate, dest = read_amount(amount)

    price_date = arrow.get(date + ' ' + time)

    return Price(timestamp=price_date, source=src, dest=dest, rate=rate)


def read_ignore_symbol_line(line: str) -> IgnoreSymbol:
    "Reads a line that specifies an ignored symbol"
    _, symbol = line.split(maxsplit=1)
    return IgnoreSymbol(symbol=symbol)


def read_default_commodity_line(line: str) -> DefaultCommodity:
    "Reads a line that specifies the default commodity"
    _, amount = line.split(maxsplit=1)
    _, commodity = read_amount(amount)
    return DefaultCommodity(commodity)


def read_lines(iterator: Iterator[str]) -> Iterator:
    """
    Reads all lines from the iterator and builds and yields the journal
    objects that are parsed
    """
    current_transaction = None
    for line in iterator:
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


def read_file(filename: str) -> Iterator:
    """
    Generates journal objects from the file at with the given filename,
    following any `include` directives within
    """
    iterator = load_lines(filename)
    iterator = remove_comments(iterator)
    iterator = remove_empty_lines(iterator)
    yield from read_lines(iterator)
