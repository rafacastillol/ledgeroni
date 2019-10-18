"""
print.py: Defines the `print` subcommand
"""
import click
from ledgeroni.journal import Journal
from ledgeroni import query


@click.command()
@click.argument('filter_strs', nargs=-1)
@click.pass_context
def print_transactions(ctx, filter_strs):
    "`ledgeroni print` subcommand"
    filter_query = None
    if filter_strs:
        filter_query = query.build_simple_or_query(filter_strs)

    sorter = ctx.obj.get('SORTER', None)
    journal = Journal(query=filter_query)
    price_db = ctx.obj.get('PRICE_DB', None)
    if price_db:
        journal.add_from_file(price_db)

    for filename in ctx.obj.get('LEDGER_FILES', []):
        journal.add_from_file(filename)

    if sorter:
        sorter.sort_journal(journal)

    click.echo('\n\n'.join(t.as_journal_format()
                           for t in journal.transactions))
