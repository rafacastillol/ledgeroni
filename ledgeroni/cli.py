import click
from ledgeroni.commands.balance import print_balance
from ledgeroni.commands.print import print_transactions
from colorama import init
init()

@click.group()
@click.option('--ledger-files', '--file', '-f', multiple=True, help='ledger files')
@click.option('--price-db', help='price database')
@click.pass_context
def cli(ctx, ledger_files, price_db):
    ctx.obj = {}
    if ledger_files:
        ctx.obj['LEDGER_FILES'] = ledger_files
    if price_db:
        ctx.obj['PRICE_DB'] = price_db

cli.add_command(print_balance, name='balance')
cli.add_command(print_balance, name='bal')
cli.add_command(print_transactions, name='print')
