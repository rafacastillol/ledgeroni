from ledgeroni import aggregate
from ledgeroni.aggregate import AccountAggregate
from collections import defaultdict
from ledgeroni.types import (Transaction, Posting, Commodity, Price,
                                   IgnoreSymbol, DefaultCommodity)

USD = Commodity(is_prefix=True, name='$')

class TestAccountAggregate:
    def test_build_from_dict_tree(self):
        expected = AccountAggregate(name=None,
                own_balances=defaultdict(int),
            subaccounts={'Bank': AccountAggregate(
                own_balances=defaultdict(int),
                subaccounts={'Paypal': AccountAggregate(
                                own_balances=defaultdict(int),
                                subaccounts={},
                                aggregates=defaultdict(int)),
                             'Bancomer': AccountAggregate(
                                 own_balances=defaultdict(int),
                                 subaccounts={},
                                 aggregates=defaultdict(int))},
                aggregates=defaultdict(int))},
            aggregates=defaultdict(int))
        tree = {'Bank': {'Paypal': {}, 'Bancomer': {}}}
        agg = aggregate.AccountAggregate.build_from_dict_tree(None, tree)
        assert expected == agg

    def test_build_from_accounts(self):
        accounts = [('Bank', 'Paypal'), ('Bank', 'Bancomer')]
        agg = AccountAggregate.build_from_accounts(accounts)
        expected = AccountAggregate(name=None,
                own_balances=defaultdict(int),
            subaccounts={'Bank': AccountAggregate(
                own_balances=defaultdict(int),
                subaccounts={'Paypal': AccountAggregate(
                                own_balances=defaultdict(int),
                                subaccounts={},
                                aggregates=defaultdict(int)),
                             'Bancomer': AccountAggregate(
                                 own_balances=defaultdict(int),
                                 subaccounts={},
                                 aggregates=defaultdict(int))},
                aggregates=defaultdict(int))},
            aggregates=defaultdict(int))
        assert expected == agg

    def test_build_from_accounts(self):
        accounts = [('Bank', 'Paypal'), ('Bank', 'Bancomer')]
        agg = AccountAggregate.build_from_accounts(accounts)
        agg.add_commodity(('Bank', 'Paypal'), 100, 'USD')
        agg.add_commodity(('Bank',), 100, 'USD')
        print(agg)

