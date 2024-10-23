import textwrap

from django import template

register = template.Library()


@register.filter
def format_phone(number):
    "0000000000 => 00 00 00 00 00"
    if len(number) == 10:
        split_number = textwrap.wrap(number, 2)
        return " ".join(split_number)
    return number


@register.filter
def format_attachment(path):
    return path.split("/")[-1]
