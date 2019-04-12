from django.template import Library

register = Library()

@register.filter('multiply')
def multiply(value,arg):
    return int(value)*int(arg)














