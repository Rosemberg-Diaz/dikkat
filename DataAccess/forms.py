from django import forms
from .models import User, restaurante, plato, producto, inventario
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name', 'last_name', 'rol','restaurante']

class productPlatoForm(forms.ModelForm):

    class Meta:
        model = inventario
        fields = ['cantidadGastada']


class restauranteForm(forms.ModelForm):

    class Meta:
        model = restaurante
        fields = ['nombre','descripcion','telefono','cantidadMesas','instagram','facebook','twiter','lunes','martes','miercoles','jueves','viernes','sabado','domingo']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'telefono': 'Teléfono',
            'cantidadMesas': 'Cantidad de Mesas',
            'instagram': 'Instagram URL',
            'facebook': 'Facebook URL',
            'twitter': 'Twitter URL',
            'lunes': 'Horario del Lunes en formato (hora inicio-hora final)',
            'martes': 'Horario del Martes en formato (hora inicio-hora final)',
            'miercoles': 'Horario del Miércoles en formato (hora inicio-hora final)',
            'jueves': 'Horario del Jueves en formato (hora inicio-hora final)',
            'viernes': 'Horario del Viernes en formato (hora inicio-hora final)',
            'sabado': 'Horario del Sábado en formato (hora inicio-hora final)',
            'domingo': 'Horario del Domingo en formato (hora inicio-hora final)',
        }


    def clean(self):

        # data from the form is fetched using super function
        super(restauranteForm, self).clean()

        # extract the username and text field from the data
        descripcion = self.cleaned_data.get('descripcion')
        nombre = self.cleaned_data.get('nombre')

        # conditions to be met for the username length
        if len(descripcion) < 10:
            self._errors['descripcion'] = self.error_class([
                'Debe contener un minimo de 10 caracteres'])
        if len(nombre) < 5:
            self._errors['nombre'] = self.error_class([
                'Debe contener un minimo de 5 caracteres'])

        # return any errors if found
        return self.cleaned_data

        # Agrega la clase personalizada a los div generados por as_div
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['nombre','descripcion','telefono','cantidadMesas','instagram','facebook','twiter','lunes','martes','miercoles','jueves','viernes','sabado','domingo']:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control ml-3 mb-4'

class productoForm(forms.ModelForm):

    class Meta:
        model = producto
        fields = ['nombre','precio','unidadMedida','estado','cantidadDisponible']

    # def __init__(self, *args, **kwargs):
    #     super(productoForm, self).__init__(*args, **kwargs)
    #     self.fields['restaurante'].disabled = True
    #     # this function will be used for the validation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['nombre','precio','unidadMedida','estado','cantidadDisponible']:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control ml-3 mb-4'

    def clean(self):

        # data from the form is fetched using super function
        super(productoForm, self).clean()

        # extract the username and text field from the data
        precio = self.cleaned_data.get('precio')
        nombre = self.cleaned_data.get('nombre')
        cantidadDisponible = self.cleaned_data.get('cantidadDisponible')

        # conditions to be met for the username length
        if precio < 0:
            self._errors['precio'] = self.error_class([
                'Debe ser un numero positivo'])
        if cantidadDisponible < 0:
            self._errors['cantidadDisponible'] = self.error_class([
                'Debe ser un numero positivo'])
        if len(nombre) < 5:
            self._errors['nombre'] = self.error_class([
                'Debe contener un minimo de 5 caracteres'])

        # return any errors if found
        return self.cleaned_data

class CorreoForm(forms.Form):
    correo = forms.EmailField(label='Correo Electrónico')

    def __init__(self, *args, **kwargs):
        super(CorreoForm, self).__init__(*args, **kwargs)
        for field_name in ['correo']:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control ml-3 mb-4'

class MesaForm(forms.Form):
    correo = forms.EmailField(label='Correo Electrónico')

    def __init__(self, num_choices=3, *args, **kwargs):
        super(MesaForm, self).__init__(*args, **kwargs)
        self.fields['numero'] = forms.ChoiceField(
            choices=[(i, str(i)) for i in range(1, num_choices + 1)],
            label='Selecciona el numero de mesa en la que te encuentras'
        )
        for field_name in ['numero','correo']:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control w-100 ml-3 mb-4'
class pagoForm(forms.Form):
    METODO_PAGO_CHOICES = (
        ('efectivo', 'Efectivo'),
        ('datafono', 'Datafono'),
    )
    metodo_pago = forms.ChoiceField(choices=METODO_PAGO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

class platoForm(forms.ModelForm):

    class Meta:
        model = plato
        fields = ['nombre','descripcion','estacion','especial','precio']

    labels = {
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "estacion": "Estacion",
        "especial": "Especial",
        "precio": "Precio",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['nombre','descripcion','estacion','especial','precio']:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control ml-3 mb-4'

    def clean(self):

        # data from the form is fetched using super function
        super(platoForm, self).clean()

        # extract the username and text field from the data
        precio = self.cleaned_data.get('precio')
        descripcion = self.cleaned_data.get('descripcion')
        nombre = self.cleaned_data.get('nombre')

        # conditions to be met for the username length
        if precio < 0:
            self._errors['precio'] = self.error_class([
                'Debe ser un numero positivo'])
        if len(descripcion) < 10:
            self._errors['descripcion'] = self.error_class([
                'Debe contener un minimo de 10 caracteres'])
        if len(nombre) < 5:
            self._errors['nombre'] = self.error_class([
                'Debe contener un minimo de 5 caracteres'])

        # return any errors if found
        return self.cleaned_data

    class CorreoForm(forms.Form):
        correo = forms.EmailField(label='Correo Electrónico')

        def __init__(self, num_choices=3, *args, **kwargs):
            super(CorreoForm, self).__init__(*args, **kwargs)
            self.fields['numero'] = forms.ChoiceField(
                choices=[(i, str(i)) for i in range(1, num_choices + 1)],
                label='Selecciona un número'
            )

