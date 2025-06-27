from django import forms

class BipagemForm(forms.Form):
    nome_formulario = 'Bipagem'
    estado = forms.ChoiceField(choices=[('' , ''), ('GOOD', 'GOOD'), ('BAD', 'BAD'), ('OBSOLETO', 'OBSOLETO'),
                                        ('TRIAGEM', 'TRIAGEM'),], label='Estado')
    modelo = forms.CharField(label='Modelo', max_length=100)
    
    patrimonio = forms.CharField(label='Patrimônio', max_length=100, required=False)