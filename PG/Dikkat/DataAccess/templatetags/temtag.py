from django import template
register = template.Library()

@register.filter
def indexId(indexable, i):
    return indexable[i].id

@register.filter
def indexNombre(indexable, i):
    return indexable[i].nombre

@register.filter
def indexDes(indexable, i):
    return indexable[i].descripcion

@register.filter
def indexPrecio(indexable, i):
    return indexable[i].precio

@register.filter
def index(indexable, i):
    return indexable[i]