# Ledgeroni

[![Build Status](https://travis-ci.org/rafacastillol/ledgeroni.svg?branch=master)](https://travis-ci.org/rafacastillol/ledgeroni)

Ledgeroni is a barebones tool for working with [ledger
journals](https://www.ledger-cli.org/). It mostly exists as an educational toy,
but I think it's neat.

It tries to imitate the reference Ledger CLI in usage, but only implements the
tiniest subset of its functionality.

The name Ledgeroni was chosen because I like it better than Ledgerino.

## Instalation

**NOTE:** Make sure you have python>=3.7 installed.

To install the tool, simply clone the repository and install with pip:

```shell
$ git clone https://github.com/rafacastillol/ledgeroni.git
$ cd ledgeroni && pip install .
```

After this, you can start playing with the CLI, for example, this command will print
out the balances of the assets of the included sample journal:

```shell
$ ledgeroni -f tests/sample_data/index.ledger --price-db tests/sample_data/prices_db bal Asset
```

This command shows a registry of Expenses that are not from Reddit:

```shell
$ ledgeroni -f tests/sample_data/index.ledger --price-db tests/sample_data/prices_db bal Expense and not Reddit
```


## Development

To install and test for development, instead install using the `editable` flag:

```shell
$ pip install -r requirements.txt
$ pip install --editable .
```

Tests can be run with pytest:

```shell
$ pytest
```


