from django import template

register=template.Library()

@register.simple_tag
def sumproject(value):
    print(value)
    sum = ""
    newvalue=float(value)
    sum=0
    sum += newvalue
    return sum 