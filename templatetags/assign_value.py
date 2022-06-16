from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@stringfilter
def assign_variable(request, value):
    """To assign value to a variable in templates"""
    request.user.type = value
    return request.user.type

register.filter(assign_variable)