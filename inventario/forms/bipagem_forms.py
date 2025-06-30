from django import forms

class BipagemForm(forms.Form):
    nome_formulario = 'Bipagem'

    serial = forms.CharField(label='Serial', max_length=100)
    modelo = forms.CharField(label='Modelo', max_length=100, required=False)
    patrimonio = forms.CharField(label='Patrimônio', max_length=100, required=False)
    estado = forms.ChoiceField(
        required=False,
        choices=[('', ''), ('GOOD', 'GOOD'), ('BAD', 'BAD'), ('OBSOLETO', 'OBSOLETO'), ('TRIAGEM', 'TRIAGEM')],
        label='Estado'
    )