import click
from ledgeroni.journal import Journal
from ledgeroni.aggregate import AccountAggregate
from ledgeroni import query
from pprint import pprint
from colorama import Fore, Back, Style
import colorama

colorama.init()


def format_amount(commodity, amount):
    s = commodity.format_amount(amount)
    s = '{:>20}'.format(s)
    if amount < 0:
        s = Fore.RED + s + Style.RESET_ALL
    return s


@click.command()
@click.argument('filter_strs', nargs=-1)
@click.pass_context
def print_balance(ctx, filter_strs):
    filter_query = (None if not filter_strs 
                    else query.build_simple_or_query(filter_strs))
    journal = Journal(query=filter_query,
                      aggregate = AccountAggregate(),
                      only_filter_transactions=False) 
    price_db = ctx.obj.get('PRICE_DB', None)
    if price_db:
        journal.add_from_file(price_db)

    for filename in ctx.obj.get('LEDGER_FILES', []):
        journal.add_from_file(filename)

    balances = list(journal.aggregate.iter_aggregates())
    _, _, total = balances[0]
    balances = balances[1:]
    for level, name, aggregate in balances:
        lvlstr = '\n'.join(format_amount(c, a)
                           for c, a in aggregate.items())
        lvlstr += '  ' * level + Fore.BLUE + name + Style.RESET_ALL
        click.echo(lvlstr)
    click.echo('-' * 20)
    totalstr = '\n'.join(format_amount(c, a)
                         for c, a in total.items())
    click.echo(totalstr)
