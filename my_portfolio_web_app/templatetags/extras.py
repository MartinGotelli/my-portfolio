from django.utils.safestring import SafeString
from django import template

register = template.Library()


def _number_html(number, positive_class, negative_class, zero_class):
    _number = float(number)
    if _number > 0:
        style = positive_class
    elif _number < 0:
        style = negative_class
    else:
        style = zero_class

    return SafeString(f'<td class="{style}">{number}</td>')


@register.filter
def number_html(number):
    return _number_html(number, 'num-green', 'num-red', 'num-gray')


@register.filter
def bold_number_html(number):
    return _number_html(number, 'num-bold-green', 'num-bold-red', 'num-bold')
