from django import forms
from hfgame.models import Game, Name

# Create the form class.
class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['text','descr']

class GameStatusForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['status']

class NameForm(forms.Form):
    name = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
