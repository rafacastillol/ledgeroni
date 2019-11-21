"""
print.py: Defines the `print` subcommand
"""
import sys
import click
from ledgeroni.journal import Journal
from ledgeroni import expression
from ledgeroni.query import MATCH_ALL


@click.command()
@click.argument('filter_strs', nargs=-1)
@click.pass_context
def print_transactions(ctx, filter_strs):
    "`ledgeroni print` subcommand"
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

    click.echo('\n\n'.join(t.as_journal_format() for t in
                           journal.transactions_matching(filter_query)))
