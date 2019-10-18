import click
import itertools
from colorama import Fore, Back, Style

from ledgeroni.journal import Journal
from ledgeroni.util import format_amount


def build_table(transaction, postings):
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
        for change, total in itertools.zip_longest(changes, totals, fillvalue=' ' * 20):
            line[2], line[3] = change, total
            yield tuple(line)
            line[0] = Style.BRIGHT + Style.RESET_ALL
            line[1] = Fore.BLUE + Style.RESET_ALL


@click.command()
@click.argument('filter_strs', nargs=-1)
@click.pass_context
def print_register(ctx, filter_strs):
    filter_query = (None if not filter_strs 
                    else query.build_simple_or_query(filter_strs))
    sorter = ctx.obj.get('SORTER', None)
    journal = Journal(query=filter_query)
    price_db = ctx.obj.get('PRICE_DB', None)
    if price_db:
        journal.add_from_file(price_db)

    for filename in ctx.obj.get('LEDGER_FILES', []):
        journal.add_from_file(filename, calc_totals=False)


    for transaction, postings in journal.generate_running_total_report():
        for trans, post, change, total in build_table(transaction, postings):
            click.echo('{:<64} {:<50} {} {}'.format(
                trans, post, change, total))
