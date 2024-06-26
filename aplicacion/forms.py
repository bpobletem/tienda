# forms.py
from django import forms
from .models import Usuario, Direccion, Zapatilla, StockZapatilla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'detalle', 'comuna', 'region']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['detalle'].required = False


class AdminLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_superuser:
            raise forms.ValidationError("Solo los administradores pueden acceder a esta página.")


class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
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
    
class UpdateUsuarioForm(forms.ModelForm):
    fnac = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'fnac', 'telefono']
    
class ZapatillaForm(forms.ModelForm):
    class Meta:
        model = Zapatilla
        fields = ['marca', 'modelo', 'precio', 'categoria', 'descripcion', 'foto']

    def __init__(self, *args, **kwargs):
        super(ZapatillaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Agregar Zapatilla'))

class StockZapatillaForm(forms.ModelForm):
    class Meta:
        model = StockZapatilla
        fields = ['zapatilla', 'talla', 'cantidad']

    def __init__(self, *args, **kwargs):
        super(StockZapatillaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Agregar Stock'))