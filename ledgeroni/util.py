"""
Utilities for working with ledger types
"""
from colorama import Fore, Style


def safe_format_amount(commodity, amount):
    """
    Formats an amount with a commodity, or without it if the commodity is None
    """
    if commodity is None:
        return str(amount)
    return commodity.format_amount(amount)


def format_amount(commodity, amount):
    "Formats the given amount for final display"
    fmted = safe_format_amount(commodity, amount)
    fmted = '{:>20}'.format(fmted)
    if amount < 0:
        fmted = Fore.RED + fmted + Style.RESET_ALL
    return fmted
