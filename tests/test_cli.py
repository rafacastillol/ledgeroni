from click.testing import CliRunner
from ledgeroni.cli import cli

def test_balance():
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'bal', 'Expense'])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'balance', 'Expense'])
    assert result.exit_code == 0


def test_print():
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'print', 'Expense'])
    assert result.exit_code == 0


def test_register():
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'register', 'Expense'])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'reg', 'Expense'])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'r', 'Expense'])
    assert result.exit_code == 0
