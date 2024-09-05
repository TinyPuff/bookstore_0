from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def reduce_one(value):
    value -= 1
    return value
