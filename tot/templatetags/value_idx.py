from django import template
# from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter
def value_by_key(d, key):
    return d[key]
