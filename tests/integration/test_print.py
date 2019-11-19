from click.testing import CliRunner
from ledgeroni.cli import cli


def test_printing():
    "Tests print command output without extra options"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'print'])
    assert result.exit_code == 0
    assert "Sold some bitcoins" in result.output
    assert "I owe Joe for a favor" in result.output


def test_filtering():
    "Tests print command output with a filter specified"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'print', 'Expense'])
    assert result.exit_code == 0
    assert 'Sold some bitcoins' not in result.output
    assert 'Purchased reddit gold for the year' in result.output
    assert 'I owe Joe for a favor' in result.output


def test_without_ledger():
    "Throws an error when no ledger file is specified"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '--price-db', 'tests/sample_data/prices_db', 'balance'])
    assert result.exit_code == 2
