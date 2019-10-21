"""
balance.py: Defines the `balance` subcommand
"""
import click
from colorama import Fore, Style

from ledgeroni.journal import Journal
from ledgeroni.aggregate import AccountAggregate
from ledgeroni.util import format_amount
from ledgeroni import expression

@click.command()
@click.argument('filter_strs', nargs=-1)
@click.pass_context
def print_balance(ctx, filter_strs):
    "`ledger balance` subcommand"
    filter_query = None
    if filter_strs:
        filter_query = expression.build_expression(' '.join(filter_strs))
    journal = Journal(query=filter_query)

    aggregate = AccountAggregate()

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

    aggregate.add_from_journal(journal)

    balances = list(aggregate.iter_aggregates())
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
