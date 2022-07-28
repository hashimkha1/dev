from django import template
import re,json
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def splitHyperLink(data,rtype="urlname"):
    result = re.split(r'=HYPERLINK\("(.*?)","(.*?)"\)', data)
    if rtype == "url":
        return result[1]
    else:
        return result[2]

@register.filter()
def range(minimum,maximum):
    print(minimum,maximum)
    return range(minimum,maximum)

@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)