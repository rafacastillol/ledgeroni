"""
register.py: Defines the `register subcommand`
"""
import itertools
from os import sys
import click
from colorama import Fore, Style

from ledgeroni.journal import Journal
from ledgeroni.util import format_amount
from ledgeroni import expression
from ledgeroni.query import MATCH_ALL


def build_table(transaction, postings):
    "Generates the register table line by line"
    # This whole thing stinks, fix it
    line = [''] * 4

    line[0] = (transaction.date_str + ' ' + Style.BRIGHT +
               transaction.description + Style.RESET_ALL)
    for posting, amts in postings.items():
        line[1] = Fore.BLUE + posting + Style.RESET_ALL

        changes, totals = amts
        changes = [format_amount(c, a) for c, a in changes.items()]
        if totals:
            totals = [format_amount(c, a) for c, a in totals.items()]
        else:
            totals = ['{:>20}'.format('0')]
        for change, total in itertools.zip_longest(changes, totals,
                                                   fillvalue=' ' * 20):
            line[2], line[3] = change, total
            yield tuple(line)
            line[0] = Style.BRIGHT + Style.RESET_ALL
            line[1] = Fore.BLUE + Style.RESET_ALL


@click.command()
@click.argument('filter_strs', nargs=-1)
@click.pass_context
def print_register(ctx, filter_strs):
    "The `ledgeroni print` subcommand"
    filter_query = MATCH_ALL
    if filter_strs:
        filter_query = expression.build_expression(' '.join(filter_strs))
    sorter = ctx.obj.get('SORTER', None)

    journal = Journal()

    price_db = ctx.obj.get('PRICE_DB', None)
    if price_db:
        journal.add_from_file(price_db)

    for filename in ctx.obj.get('LEDGER_FILES', []):
        journal.add_from_file(filename)

    errors = journal.verify_transaction_balances()
    if errors:
        for error in errors:
            errstr = 'ERROR! Transaction unbalanced: {}'.format(error.header)
            click.echo(errstr, err=True)
        sys.exit(1)

    if sorter:
        sorter.sort_journal(journal)

    for transaction, postings in journal.generate_running_total_report(filter_query):
        for trans, post, change, total in build_table(transaction, postings):
            click.echo('{:<64} {:<50} {} {}'.format(
                trans, post, change, total))
