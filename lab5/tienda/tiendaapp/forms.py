from django.forms import ModelForm
from .models import *
class RegistroForm(ModelForm):
    #password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())
    class Meta:
        model = Cliente
        fields = ('username', 'password', 'CliDNI', 'CliApePat', 'CliNom', 'CliEstReg')
