from colorama import Fore, Back, Style

def safe_format_amount(commodity, amount):
    if commodity is None:
        return amount
    return commodity.format_amount(amount)

def format_amount(commodity, amount):
    s = safe_format_amount(commodity, amount)
    s = '{:>20}'.format(s)
    if amount < 0:
        s = Fore.RED + s + Style.RESET_ALL
    return s
