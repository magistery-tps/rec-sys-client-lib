from django import template

register = template.Library()

@register.filter(name='field_type')
def sanitize_tags(field):
    return field.field.widget.__class__.__name__