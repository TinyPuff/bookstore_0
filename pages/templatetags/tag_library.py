from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def reduce_one(value):
    value -= 1
    return value

@register.filter()
def conv_list(arg):
    return list(arg)