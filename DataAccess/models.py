from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import numeroValido
from django.contrib.auth.models import AbstractUser

class restaurante(models.Model):
    """
    Modelo que representa un restaurante.

    Atributos:
        - nombre (str): El nombre del restaurante (campo único).
        - descripcion (str): Una descripción opcional del restaurante.
        - telefono (str): Número de teléfono del restaurante (validado con `numeroValido`).
        - logo (str): URL o ruta al logo del restaurante.
        - cantidadMesas (int): Cantidad de mesas en el restaurante.
        - instagram (str): Nombre de usuario de Instagram del restaurante.
        - facebook (str): Nombre de usuario de Facebook del restaurante.
        - twiter (str): Nombre de usuario de Twitter del restaurante.
        - lunes (str): Horario o detalles para los lunes.
        - martes (str): Horario o detalles para los martes.
        - miercoles (str): Horario o detalles para los miércoles.
        - jueves (str): Horario o detalles para los jueves.
        - viernes (str): Horario o detalles para los viernes.
        - sabado (str): Horario o detalles para los sábados.
        - domingo (str): Horario o detalles para los domingos.

    Métodos:
        - __str__(): Devuelve el nombre del restaurante como representación de cadena.
    """

    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=1000, default="")
    telefono = models.CharField(max_length=200, validators=[numeroValido])
    logo = models.TextField(default="X")
    cantidadMesas = models.PositiveIntegerField()
    instagram = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200)
    twiter = models.CharField(max_length=200)
    lunes = models.CharField(max_length=200)
    martes = models.CharField(max_length=200)
    miercoles = models.CharField(max_length=200)
    jueves = models.CharField(max_length=200)
    viernes = models.CharField(max_length=200)
    sabado = models.CharField(max_length=200)
    domingo = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class user(AbstractUser):
    """
    Modelo que extiende el modelo de usuario de Django con roles personalizados.

    Atributos:
        - rol (str): El rol del usuario (elección entre BEBIDA, PRINCIPAL, POSTRE, CAJA).
        - restaurante (ForeignKey): Relación con el modelo Restaurante.
        - isAdminRest (bool): Indica si el usuario es administrador de un restaurante.

    Métodos:
        - __str__(): Devuelve el nombre de usuario como representación de cadena.
    """

    class Rol(models.TextChoices):
        BEBIDA = 'Bebida', ('Bebida')
        PRINCIPAL = 'Principal', ('Principal')
        POSTRE = 'Postre', ('Postre')
        CAJA = 'Dueño', ('Dueño')
        __empty__ = ('Seleccione')

    rol = models.CharField(choices=Rol.choices, max_length=200)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)
    isAdminRest = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class producto(models.Model):
    """
    Modelo que representa un producto.

    Atributos:
        - nombre (str): El nombre del producto.
        - precio (float): El precio del producto (validado con MinValueValidator).
        - unidadMedida (str): Unidad de medida del producto (elección entre LITROS y LIBRAS).
        - estado (str): Estado del producto (elección entre DISPONIBLE y AGOTADO).
        - cantidadDisponible (float): Cantidad disponible del producto (validado con MinValueValidator).
        - restaurante (ForeignKey): Relación con el modelo Restaurante.
        - imagenInv (str): URL o ruta de la imagen del producto.

    Métodos:
        - __str__(): Devuelve el nombre del producto como representación de cadena.
    """

    class Estado(models.TextChoices):
        DISPONIBLE = 'Disponible', ('Disponible')
        AGOTADO = 'Agotado', ('Agotado')
        __empty__ = ('Seleccione')

    class UnidadMedida(models.TextChoices):
        LITROS = 'Litros', ('Litros')
        LIBRAS = 'Libras', ('Libras')
        __empty__ = ('Seleccione')

    nombre = models.CharField(max_length=200)
    precio = models.FloatField(validators=[MinValueValidator(0.0)])
    unidadMedida = models.CharField(choices=UnidadMedida.choices, max_length=200)
    estado = models.CharField(choices=Estado.choices, max_length=200, default="Disponible")
    cantidadDisponible = models.FloatField(validators=[MinValueValidator(0.0)])
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)
    imagenInv = models.TextField(default="X")

    def __str__(self):
        return self.nombre

class plato(models.Model):
    """
    Modelo que representa un plato.

    Atributos:
        - nombre (str): El nombre del plato.
        - estacion (str): Estación a la que pertenece el plato (elección entre BEBIDA, PRINCIPAL y POSTRE).
        - especial (bool): Indica si el plato es especial.
        - descripcion (str): Descripción del plato.
        - precio (float): El precio del plato (validado con MinValueValidator).
        - imagenMenu (str): URL o ruta de la imagen del plato.
        - restaurante (ForeignKey): Relación con el modelo Restaurante.

    Métodos:
        - __str__(): Devuelve el nombre del plato como representación de cadena.
    """

    class Estacion(models.TextChoices):
        BEBIDA = 'Bebida', ('Bebida')
        PRINCIPAL = 'Principal', ('Principal')
        POSTRE = 'Postre', ('Postre')
        __empty__ = ('Seleccione')

    nombre = models.CharField(max_length=200)
    estacion = models.CharField(choices=Estacion.choices, max_length=200)
    especial = models.BooleanField(default=True)
    descripcion = models.TextField(max_length=500)
    precio = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    imagenMenu = models.TextField(default="X")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class inventario(models.Model):
    """
    Modelo que representa un registro de inventario.

    Atributos:
        - restaurante (ForeignKey): Relación con el modelo Restaurante.
        - producto (ForeignKey): Relación con el modelo Producto.
        - plato (ForeignKey): Relación con el modelo Plato.
        - cantidadGastada (float): Cantidad gastada en el inventario (validado con MinValueValidator).
    """

    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, null=True, blank=True)
    cantidadGastada = models.FloatField(validators=[MinValueValidator(0.0)])

class orden(models.Model):
    """
    Modelo que representa una orden.

    Atributos:
        - identificator (str): Identificador único de la orden.
        - restaurante (ForeignKey): Relación con el modelo Restaurante.
        - plato (ForeignKey): Relación con el modelo Plato.
        - mesa (int): Número de mesa.
        - cantidad (int): Cantidad de platos en la orden.
        - estado (bool): Estado de la orden (True si está activa, False si está inactiva).
        - pagado (bool): Indica si la orden ha sido pagada.
        - horaPedido (DateTime): Fecha y hora en que se realizó el pedido.
    """

    identificator = models.TextField(default="X")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, null=True, blank=True)
    mesa = models.PositiveIntegerField()
    cantidad = models.IntegerField(default=1)
    estado = models.BooleanField(default=True)
    pagado = models.BooleanField(default=False)
    horaPedido = models.DateTimeField()

class factura(models.Model):
    """
    Modelo que representa una factura.

    Atributos:
        - tipoPago (str): Tipo de pago (elección entre BEBIDA y PRINCIPAL).
        - propina (float): Monto de propina (validado con MinValueValidator).
        - total (float): Monto total de la factura (validado con MinValueValidator).
        - email (str): Correo electrónico del cliente.
        - restaurante (ForeignKey): Relación con el modelo Restaurante.
        - identificatorOrder (str): Identificador de la orden.

    Métodos:
        - __str__(): Devuelve el tipo de pago como representación de cadena.
    """

    class Pagos(models.TextChoices):
        BEBIDA = 'Tarjeta', ('Tarjeta')
        PRINCIPAL = 'Efectivo', ('Efectivo')
        __empty__ = ('Seleccione')

    tipoPago = models.CharField(choices=Pagos.choices, max_length=200)
    propina = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    total = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    email = models.EmailField()
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)
    identificatorOrder = models.CharField(choices=Pagos.choices, max_length=200, default="x")

class productosFactura(models.Model):
    """
    Modelo que relaciona productos con facturas.

    Atributos:
        - restaurante (ForeignKey): Relación con el modelo Restaurante.
        - producto (ForeignKey): Relación con el modelo Producto.
        - factura (ForeignKey): Relación con el modelo Factura.
        - cantidad (float): Cantidad de productos en la factura (validado con MinValueValidator).
    """

    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cantidad = models.FloatField(validators=[MinValueValidator(0.0)], default=1)

