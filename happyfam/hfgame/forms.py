from django import forms
from hfgame.models import Game, Name, GameStatus
from django.shortcuts import get_object_or_404

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

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        winner = cleaned_data.get('winner')

        print(status)
        print(type(status))
        print(winner)
        done = get_object_or_404(GameStatus, short='d')
        print(done)
        print(type(done))

        if status == done:
            print('status is done')
            if not winner:
                print('no winner')
                raise forms.ValidationError(
                    'Test'
                )
                # self.add_error('winner', err)
        else:
            # We know winner must be blank if status is not 3, so ensure this is the case
            print('status is not done')
            self.cleaned_data['winner'] = None

        return self.cleaned_data

class NameForm(forms.Form):
    name = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
