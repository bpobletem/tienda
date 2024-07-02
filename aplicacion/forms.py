# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Usuario, Direccion, Zapatilla, StockZapatilla, Pedido, PedidoZapatilla
from django.contrib.auth.forms import AuthenticationForm


class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100)


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
            raise forms.ValidationError(
                "Solo los administradores pueden acceder a esta página.")


class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput)
    fnac = forms.DateInput(format=(
        '%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'})

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
    fnac = forms.DateInput(format=(
        '%d-%m-%Y'), attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'})

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'fnac', 'telefono']


class ZapatillaForm(forms.ModelForm):
    class Meta:
        model = Zapatilla
        fields = ['marca', 'modelo', 'precio',
                  'categoria', 'descripcion', 'foto']
        widgets = {
            'categoria': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ZapatillaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Agregar Zapatilla'))


class StockZapatillaForm(forms.ModelForm):
    class Meta:
        model = StockZapatilla
        fields = ['talla', 'cantidad']
        exclude = ['zapatilla']

    def __init__(self, *args, **kwargs):
        super(StockZapatillaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Agregar Stock'))


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(choices=Pedido.ESTADO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar Cambios'))


class PedidoZapatillaForm(forms.ModelForm):
    class Meta:
        model = PedidoZapatilla
        fields = ['zapatilla',  'cantidad']


class PedidoEstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(choices=Pedido.ESTADO_CHOICES, attrs={'class': 'form-control'}),
        }


PedidoZapatillaFormSet = modelformset_factory(
    PedidoZapatilla, form=PedidoZapatillaForm, extra=1
)
