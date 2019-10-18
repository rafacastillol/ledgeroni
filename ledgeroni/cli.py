"""
cli.py: Main entrypoint for Click
"""
import click
from colorama import init

from ledgeroni.sorter import JournalSorter
from ledgeroni.commands.balance import print_balance
from ledgeroni.commands.print import print_transactions
from ledgeroni.commands.register import print_register

init()


@click.group()
@click.option('--ledger-files', '--file', '-f', multiple=True,
              help='ledger files')
@click.option('--price-db', help='price database')
@click.option('--sort', '-S', type=str,
              help='specifies how transactions should be sorted')
@click.pass_context
def cli(ctx, ledger_files, price_db, sort):
    "Base ledgeroni command"
    ctx.obj = {}
    if ledger_files:
        ctx.obj['LEDGER_FILES'] = ledger_files
    if price_db:
        ctx.obj['PRICE_DB'] = price_db
    if sort:
        sorter = JournalSorter.from_term_list(s.strip() for s in
                                              sort.split(','))
        ctx.obj['SORTER'] = sorter


cli.add_command(print_balance, name='balance')
cli.add_command(print_balance, name='bal')
cli.add_command(print_transactions, name='print')
cli.add_command(print_register, name='r')
cli.add_command(print_register, name='reg')
cli.add_command(print_register, name='register')
