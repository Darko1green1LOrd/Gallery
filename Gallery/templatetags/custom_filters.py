from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    return str(value).split(key)

@register.filter(name='ind')
def index(indexable, i):
    return indexable[i]
