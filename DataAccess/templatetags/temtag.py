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
def indexImagen(indexable, i):
    return indexable[i].imagenMenu

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def indexPagado(indexable, i):
    return indexable[i].pagado