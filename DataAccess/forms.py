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
        fields = ['nombre','descripcion','telefono','cantidadMesas']


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

class productoForm(forms.ModelForm):

    class Meta:
        model = producto
        fields = ['nombre','precio','unidadMedida','estado','cantidadDisponible']

    # def __init__(self, *args, **kwargs):
    #     super(productoForm, self).__init__(*args, **kwargs)
    #     self.fields['restaurante'].disabled = True
    #     # this function will be used for the validation

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

    def __init__(self, num_choices=3, *args, **kwargs):
        super(CorreoForm, self).__init__(*args, **kwargs)
        self.fields['numero'] = forms.ChoiceField(
            choices=[(i, str(i)) for i in range(1, num_choices + 1)],
            label='Selecciona un número'
        )


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
    # widgets = {
    #     "nombre": forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', "placeholder": "أدخل كلمة المرور الحالية"}),
    #     "descripcion": forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', "placeholder": "أدخل كلمة المرور الجديدة"}),
    #     "precio": forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', "placeholder": "أدخل كلمة المرور الجديدة مرة أخرى"})
    # }
    # help_texts = {
    #     'name': _('Some useful help text.'),
    # }

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

