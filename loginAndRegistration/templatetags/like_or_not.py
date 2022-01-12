from django import template

register = template.Library()


@register.filter
def liked(obj, id):
    if obj.liked.filter(id=id).exists():
        return True
    return False
