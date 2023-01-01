from django import template

register = template.Library()

@register.filter(name='sanitize_tags')
def sanitize_tags(value):
    try:
        return ', '.join([f'"{t.name}"' for t in value])
    except:
        return value
