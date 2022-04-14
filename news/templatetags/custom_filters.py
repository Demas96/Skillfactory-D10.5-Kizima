from django import template
import re

register = template.Library()


@register.filter(name='censor')
def censor(value):
    count = 0
    c_word = ['блин', 'черт']
    text = value.split()
    for i in text:
        i = i.lower()
        i = re.sub(r'[^\w\s]', '', i)
        for j in c_word:
            if i == j:
                return value.replace(text[count], '*' * len(i))
        count += 1
    return value
