from django import forms
from .models import Item, Interaction
from allauth.account.forms import LoginForm


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
    

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = "__all__"


class LikeForm:
    def __init__(self, request): self.request = request

    @property
    def item_id(self): return self.request.POST['item_id']

    @property
    def rating(self):
        if 'rating' in self.request.POST:
            return self.request.POST['rating']
        else:
            return 0

    def __str__(self):
        return f'LikeForm(item_id: {self.item_id}, rating: {self.rating})'
