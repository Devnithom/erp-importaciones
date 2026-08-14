from django import template

register = template.Library()

@register.filter(name='tiene_rol')
def tiene_rol(user, nombre_rol):
    # Si es el dueño, ve todo. Si no, busca en qué grupo está.
    if user.is_superuser:
        return True
    return user.groups.filter(name=nombre_rol).exists()