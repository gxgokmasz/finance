from django import template
from django.forms import BoundField


register = template.Library()


@register.filter()
def error_input(input: BoundField):
    return input.as_widget(attrs={"class": "input-field input-error"})
