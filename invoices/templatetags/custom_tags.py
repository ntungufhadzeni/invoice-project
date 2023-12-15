from django import template
from currency_symbols import CurrencySymbols

register = template.Library()


# An upper function that capitalizes the first letter of the word passed to it. We then register the filter using a
# suitable name.
@register.filter(name='modify_name')
def modify_name(value):
    return value.title()


@register.filter(name='upper')
def upper(value):
    return value.upper()


@register.filter()
def currency_symbol(value):
    return CurrencySymbols.get_symbol(value)


@register.filter()
def to_int(value):
    return int(value)


@register.filter()
def format_money(value):
    return f"{value:,.2f}".replace(',', ' ').replace('.', ',')


@register.filter()
def tax_amount(value):
    return value.total_amount * (value.tax_rate / 100) / (1 + value.tax_rate / 100)


@register.filter()
def sub_total(value):
    return value.total_amount / (1 + value.tax_rate / 100)


@register.filter()
def format_type(value):
    if value == 'INV':
        return 'Invoice'
    else:
        return 'Quotation'


@register.filter()
def format_address(value):
    if value:
        return value.replace('\r', ', ')
    else:
        return ''

