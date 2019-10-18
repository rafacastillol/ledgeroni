import click
from ledgeroni.sorter import JournalSorter
from ledgeroni.commands.balance import print_balance
from ledgeroni.commands.print import print_transactions
from ledgeroni.commands.register import print_register
from colorama import init
init()

@click.group()
@click.option('--ledger-files', '--file', '-f', multiple=True, help='ledger files')
@click.option('--price-db', help='price database')
@click.option('--sort', '-S', type=str, help='how transactions should be sorted')
@click.pass_context
def cli(ctx, ledger_files, price_db, sort):
    ctx.obj = {}
    if ledger_files:
        ctx.obj['LEDGER_FILES'] = ledger_files
    if price_db:
        ctx.obj['PRICE_DB'] = price_db
    if sort:
        sorter = JournalSorter.from_term_list(s.strip() for s in sort.split(','))
        ctx.obj['SORTER'] = sorter


cli.add_command(print_balance, name='balance')
cli.add_command(print_balance, name='bal')
cli.add_command(print_transactions, name='print')
cli.add_command(print_register, name='reg')
