from django import forms

from .models import Item, Evento


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'descricao', 'preco']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'data_inicial', 'data_final']
