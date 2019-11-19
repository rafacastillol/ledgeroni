from click.testing import CliRunner
from ledgeroni.cli import cli


def test_balance():
    "Tests the balance command without any options"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'balance'])
    assert result.exit_code == 0


def test_bal_alias():
    "Makes sure the balance alias is registered"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'bal'])
    assert result.exit_code == 0
    assert "1.50 BTC  Asset:Bitcoin Wallet" in result.output


def test_without_ledger():
    "Throws an error when no ledger file is specified"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '--price-db', 'tests/sample_data/prices_db', 'balance'])
    assert result.exit_code == 2
