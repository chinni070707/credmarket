from django import template

register = template.Library()

@register.filter
def replace_with_space(value):
    """Replace underscores with spaces for better readability"""
    return value.replace('_', ' ')
