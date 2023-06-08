from datetime import datetime

from django import template

register = template.Library()

@register.filter(name='iso_to_datetime')
def iso_to_datetime(value):
    return datetime.fromisoformat(value)
