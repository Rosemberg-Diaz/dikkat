from django.core.exceptions import ValidationError

def numeroValido(value):
    if (value.isalpha()):
        raise ValidationError('Debe ser un numero valido')