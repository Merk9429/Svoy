from django import template

register = template.Library()

bad_words = ['беспредел']


@register.filter(name='censor')
def censor(value):
    for word in bad_words:
        value = value.replace(word, word[0:1] + '*' * len(word))
    return value
