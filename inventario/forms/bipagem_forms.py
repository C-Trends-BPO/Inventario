from django import forms

class BipagemForm(forms.Form):
    nome_formulario = 'Bipagem'
    modelo = forms.CharField(label='Modelo', max_length=100)
    patrimonio = forms.CharField(label='Patrimônio', max_length=100)