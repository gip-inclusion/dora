from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def environment():
    return settings.ENVIRONMENT


@register.simple_tag
def frontend_url():
    return settings.FRONTEND_URL


@register.simple_tag
def support_link():
    return settings.SUPPORT_LINK
