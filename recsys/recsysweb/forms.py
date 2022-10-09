from django import forms
from .models import Item, Interaction


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
    

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = "__all__"