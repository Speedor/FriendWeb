from django import template

register = template.Library()

@register.simple_tag()
def active_css(id, permission):
    print id, permission
    if pow(2,id) == (pow(2,id) & permission):
        return ' active'
    else:
        return ''

register.filter(active_css)