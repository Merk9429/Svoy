from datetime import datetime
from django import template

register = template.Library()

bad_words = ['беспредел', 'шлак', 'Шлак']


@register.filter(name='censor')
def censor(value):
    for word in bad_words:
        value = value.replace(word, word[0:1] + '*' * len(word))
    return value


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)
