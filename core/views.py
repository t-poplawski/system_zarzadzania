from django import forms
from django.shortcuts import render, redirect
from core.models import RokAkademicki

# Create your views here.
class WyborRokuForm(forms.Form):
    rok = forms.ModelChoiceField(queryset=RokAkademicki.objects.all(), label='Wybierz rok akademicki')

def home(request):
    return render(request, 'core/home.html')

def tabela_view(request, rok, tabela):
    return render(request, f'core/{tabela}.html', {
        'rok': rok,
        'rok_slash': rok.replace('-', '/'),
        'tabela': tabela,
    })
