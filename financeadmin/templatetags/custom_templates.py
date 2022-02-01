from django import template

register=template.Library()

@register.simple_tag
def sum(value):
    print(value)
    sum=0
    sum += value
    return sum 