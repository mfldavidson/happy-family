from django import forms
from hfgame.models import Game, Name, GameStatus
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.conf import settings

# Create the form class.
class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['text','descr']

class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['text','descr','owner']

class GameStatusForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['status','winner']
        widgets = {
            'status': forms.HiddenInput(),
        }

    def clean(self):
        '''
        Custom validation to ensure that Game cannot be changed to Done without setting a winner. Note that in GameDetailView the status is changed manually AFTER clean is called via is_valid, so here we are checking if the status is In Play, knowing that the status will be changed to Done if the form is valid.
        '''
        self.cleaned_data = super().clean()
        winner = self.cleaned_data.get('winner')
        status = self.cleaned_data.get('status')

        inplay = GameStatus.objects.get(id=2)

        if status == inplay:
            if len(winner) == 0:
                raise ValidationError({'winner':('To end the game, you must select at least one winner')})

        return self.cleaned_data

class NameForm(forms.Form):
    name = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
