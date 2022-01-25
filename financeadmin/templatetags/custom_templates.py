from django import template

register=template.Library()

@register.simple_tag
def sumproject(value):
    print(value)
    sum=0
    sum +=value
    return sum 