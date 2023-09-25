from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import numeroValido
from django.contrib.auth.models import AbstractUser

class restaurante(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=1000, default="")
    telefono = models.CharField(max_length=200, validators=[numeroValido])
    logo = models.TextField(default="X")
    cantidadMesas = models.PositiveIntegerField(default=4)
    def __str__(self):
        return self.nombre

class User(AbstractUser):
    class rol(models.TextChoices):
        BEBIDA = 'Bebida', ('BEBIDA')
        PRINCIPAL = 'Principal', ('PRINCIPAL')
        POSTRE = 'Postre', ('POSTRE')
        CAJA = 'Dueño', ('CAJA')
        __empty__ = ('Seleccione')

    rol = models.CharField(choices=rol.choices,max_length=200)
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)
    isAdminRest = models.BooleanField(default=False)
    def __str__(self):
        return self.username


class producto(models.Model):
    class estado(models.TextChoices):
        DISPONIBLE = 'Disponible', ('DISPONIBLE')
        AGOTADO = 'Agotado', ('AGOTADO')
        __empty__ = ('Seleccione')

    class unidadMedida(models.TextChoices):
        LITROS = 'Litros', ('LITROS')
        LIBRAS = 'Libras', ('LIBRAS')
        __empty__ = ('Seleccione')

    nombre = models.CharField(max_length=200, unique=True)
    precio = models.FloatField(validators=[MinValueValidator(0.0)])
    unidadMedida = models.CharField(choices=unidadMedida.choices,max_length=200)
    estado = models.CharField(choices=estado.choices,max_length=200, default="Disponible")
    cantidadDisponible = models.FloatField(validators=[MinValueValidator(0.0)])
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.nombre

class plato(models.Model):
    class estacion(models.TextChoices):
        BEBIDA = 'Bebida', ('BEBIDA')
        PRINCIPAL = 'Principal', ('PRINCIPAL')
        POSTRE = 'Postre', ('POSTRE')
        __empty__ = ('Seleccione')

    nombre = models.CharField(max_length=200, unique=True)
    estacion = models.CharField(choices=estacion.choices,max_length=200)
    especial = models.BooleanField(default=True)
    descripcion = models.TextField(max_length=500)
    precio = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    imagenMenu = models.TextField(default="X")
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.nombre


class inventario(models.Model):
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE, null=True, blank=True)
    plato = models.ForeignKey(plato, on_delete=models.CASCADE, null=True, blank=True)
    cantidadGastada = models.FloatField(validators=[MinValueValidator(0.0)])

class orden(models.Model):
    identificator = models.TextField(default="X")
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)
    plato = models.ForeignKey(plato, on_delete=models.CASCADE, null=True, blank=True)
    mesa = models.PositiveIntegerField()
    cantidad = models.IntegerField(default=1)
    estado = models.BooleanField(default=True)
    horaPedido = models.DateTimeField()

class factura(models.Model):
    class pagos(models.TextChoices):
        BEBIDA = 'Tarjeta', ('TARJETA')
        PRINCIPAL = 'Efectivo', ('EFECTIVO')
        __empty__ = ('Seleccione')
    tipoPago = models.CharField(choices=pagos.choices,max_length=200)
    propina = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    total = models.FloatField(validators=[MinValueValidator(0.0)])
    email = models.EmailField()
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)

class productosFactura(models.Model):
    restaurante = models.ForeignKey(restaurante, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    factura = models.ForeignKey(factura, on_delete=models.CASCADE)
    cantidad = models.FloatField(validators=[MinValueValidator(0.0)], default=1)

