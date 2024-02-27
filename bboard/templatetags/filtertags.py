from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeText
from datetime import datetime

register = template.Library()  # for filters and tags

# filters
# @register.filter(name='cur', is_safe=True)
@register.filter(name='cur')
# @stringfilter
def currency(value, name='тг.'):
    # if not isinstance(value, SafeText):
    #     value = escape(value)
    return mark_safe(f'<strong>{value:.2f} {name}</strong>')
    # return f'<strong>{value:.2f} {name}</strong>'


# register.filter('currency', currency)


# @register.filter(expects_localtime=True)
# def datetimefilter(value):
#     pass


#tags
@register.simple_tag()
def lst(sep, *args):
    # return f'{sep.join(args)} (итого {len(args)})'
    return mark_safe(f'{sep.join(args)} (итого <strong>{len(args)}</strong>)')


# @register.simple_tag(takes_context=True)
# def lst(context, sep, *args):
#     pass


@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}


# filter #1
@register.filter
def half_string(value):
    half_length = len(value) // 2
    return value[:half_length]


# filter #2
@register.filter
def add_percent(value):
    return f'{value}%'


# filter #3
@register.filter
def uppercase(value):
    return value.upper()


# tag #1
@register.simple_tag
def split_string(string, sep):
    return string.split(sep)


# tag #2
@register.simple_tag
def current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# tag #3
@register.simple_tag
def check_list_item(item, item_list, message_if_present, message_if_not_present):
    item_list = ['apple', 'strawberry', 'banana']
    if item in item_list:
        return message_if_present
    else:
        return message_if_not_present
