from click.testing import CliRunner
from ledgeroni.cli import cli


def test_register():
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'register'])
    assert result.exit_code == 0
    assert "Sold some bitcoins" in result.output
    assert "I owe Joe for a favor" in result.output


def test_r_alias():
    "Tests whether the r alias is registered properly"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'r'])
    assert result.exit_code == 0
    assert "Sold some bitcoins" in result.output
    assert "I owe Joe for a favor" in result.output


def test_reg_alias():
    "Tests whether the reg alias is registered properly"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'reg'])
    assert result.exit_code == 0
    assert "Sold some bitcoins" in result.output
    assert "I owe Joe for a favor" in result.output


def test_filtering():
    "Tests a simple filter for the reg command"
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'tests/sample_data/index.ledger', '--price-db',
        'tests/sample_data/prices_db', 'reg', 'Expense'])
    assert result.exit_code == 0
    assert 'Sold some bitcoins' not in result.output
    assert 'Purchased reddit gold for the year' in result.output
    assert 'I owe Joe for a favor' in result.output

