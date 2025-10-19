# usuario/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil
from .models import Atleta
from .models import Treino, Exercicio
from django.forms import modelformset_factory


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Seu e-mail'})
    )
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Seu usuário'})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha'})
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita sua senha'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["idade", "peso", "altura", "meta"]
        widgets = {
            "idade": forms.NumberInput(attrs={"class": "form-control"}),
            "peso": forms.NumberInput(attrs={"class": "form-control"}),
            "altura": forms.NumberInput(attrs={"class": "form-control"}),
            "meta": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ["nome", "apelido", "idade", "peso", "altura", "objetivo"]

class TreinoForm(forms.ModelForm):
    class Meta:
        model = Treino
        fields = ['nome', 'tipo', 'dia_semana', 'duracao', 'observacoes']


class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = ['nome', 'series', 'repeticoes']


ExercicioFormSet = modelformset_factory(
    Exercicio,
    fields=('nome', 'series', 'repeticoes', 'carga'),
    extra=7,            
    max_num=7,           
    can_delete=False     
)