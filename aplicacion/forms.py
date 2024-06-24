# forms.py
from django import forms
from .models import Usuario, Direccion, Zapatilla, StockZapatilla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.core.exceptions import ValidationError


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'detalle', 'comuna', 'region']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['detalle'].required = False


class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput)
    fnac = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'correo', 'fnac', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.contrasenia = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user


class ZapatillaForm(forms.ModelForm):
    class Meta:
        model = Zapatilla
        fields = ['marca', 'modelo', 'precio',
                  'categoria', 'descripcion', 'foto']
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el modelo'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio'}),
            'categoria': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción'}),
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        error_messages = {
            'marca': {
                'required': 'Este campo es obligatorio',
            },
            'modelo': {
                'required': 'Este campo es obligatorio',
                'max_length': 'El modelo no puede tener más de 50 caracteres',
            },
            'precio': {
                'required': 'Este campo es obligatorio',
                'invalid': 'Ingrese un número válido',
            },
            'descripcion': {
                'required': 'Este campo es obligatorio',
                'max_length': 'La descripción no puede tener más de 500 caracteres',
            },
        }

    def __init__(self, *args, **kwargs):
        super(ZapatillaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('marca'),
            Field('modelo'),
            Field('precio'),
            Field('categoria'),
            Field('descripcion'),
            Field('foto'),
            Submit('submit', 'Agregar Zapatilla', css_class='btn btn-primary')
        )

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise ValidationError('El precio debe ser mayor a 0')
        return precio


class StockZapatillaForm(forms.ModelForm):
    tallas = forms.MultipleChoiceField(
        # Tallas de 7 a 11.5 en incrementos de 0.5
        choices=[(i / 2, i / 2) for i in range(14, 24)],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'talla-checkbox'}),
    )

    class Meta:
        model = StockZapatilla
        fields = ['tallas', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad'}),
        }
        error_messages = {
            'cantidad': {
                'required': 'Este campo es obligatorio',
                'invalid': 'Ingrese un número válido',
            },
        }

    def __init__(self, *args, **kwargs):
        super(StockZapatillaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('tallas', template='custom_checkbox.html'),
            Field('cantidad'),
            Submit('submit', 'Agregar Stock', css_class='btn btn-primary')
        )

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 0:
            raise ValidationError('La cantidad debe ser mayor o igual a 0')
        return cantidad
