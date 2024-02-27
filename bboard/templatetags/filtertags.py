from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeText

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


@register.filter
def half_string(value):
    half_length = int(len(value) / 2)
    return mark_safe(value[:half_length])


# @register.simple_tag
# def split_string(string, sep, *args):
#     return string.split(sep, *args)
