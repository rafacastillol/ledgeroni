"""
parser.py: parses a rudimentary verison of the ledger journal format

Details on the file format were lifted from the official documentation,
(https://www.ledger-cli.org/3.0/doc/ledger3.html#Journal-Format), however,
some features of the file were left out for simplicity's sake. Some of these
ommisions include:

* The only command directive that is accepted is `include`.
* Marking transactions as clear or pending has no effect.
* Can only specify per unit cost


"""
import re
import itertools
import arrow
from ledgeroni.transaction import Transaction

def load_lines(filename):
    with open(filename) as fp:
        for line in fp:
            if line.startswith('!include'):
                for f in line.split()[1:]:
                    yield from load_lines(f)
            else:
                yield line


def remove_comments(it):
    return (re.sub('[;#%|*].*$', '', line).rstrip() for line in it)


def remove_empty_lines(it):
    return (line for line in it if line)


def read_transaction_line(l):
    date, description = l.split(maxsplit=1)
    date = arrow.get(date)
    return Transaction(date=date, description=description)
    



def read_posting_line(l):

    l = l.strip()

    # The account name ends once we find two spaces in a row
    account, amount = l, None
    for i, c in enumerate(l[1:]):
        if l[i-1].isspace() and c.isspace():
            account, amount = l[0:i].strip(), l[i:].strip()
            break

    
    account = account.split(':')
    amount = read_amount(amount)

def read_amount(s):
    if s is None:
        return None
    parts = s.split('@')

    if len(s) == 3:
        raise ValueError
    




    

def build_transactions(it):
    current_transaction = None
    for line in it:
        if line[0].isdigit():
            if current_transaction is not None:
                yield current_transaction
            current_transaction = read_transaction_line(line)
        else:
            pass


