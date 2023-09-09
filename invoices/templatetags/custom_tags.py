from django import template
from currency_symbols import CurrencySymbols

register = template.Library()


# An upper function that capitalizes the first letter of the word passed to it. We then register the filter using a
# suitable name.
@register.filter(name='modify_name')
def modify_name(value):
    return value.title()


@register.filter(name='get_currency_symbol')
def currency_symbol(value):
    return CurrencySymbols.get_symbol(value)
