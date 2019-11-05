from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from hfgame.models import *
from hfgame.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerDeleteView
from hfgame.forms import *
from random import shuffle
import datetime

class AGamesListView(OwnerListView):
    model = Game
    template_name = "agame_list.html"

    def get(self, request) :
        game_list = Game.objects.filter(status=1).order_by('-updated_at').all()
        context = {'game_list': game_list}
        return render(request, self.template_name, context)

class HowToPlayView(View):
    template_name = 'how_to_play.html'

    def get(self, request):
        return render(request, self.template_name)

def get_game_detail_context_data(game, user, status_form):
    ''' Function to get the context data necessary for GameDetailView that stays the same between GET and POST '''

    names = list(Name.objects.filter(game=game).all())
    shuffle(names)
    name_form = NameForm()
    name_exists = Name.objects.filter(game=game, owner=user).first()
    context = {
        'game': game,
        'status_form': status_form,
        'names': names,
        'name_form': name_form,
        'name_exists': name_exists
        }
    return context

class GameDetailView(View):
    model = Game
    template_name = 'game_detail.html'

    def get(self, request, pk):
        game = Game.objects.get(id=pk)
        status_form = GameStatusForm(instance=game)
        context = get_game_detail_context_data(game, self.request.user, status_form)
        return render(request, self.template_name, context)

    def post(self, request, pk=None) :
        game = Game.objects.get(id=pk)

        status_form = GameStatusForm(self.request.POST, instance=game)

        # check if the form is valid using the custom validation in GameStatusForm.clean which checks if the winner has been set for In Play games before we change the status to Done, and return an error to the user if no winner is selected
        if not status_form.is_valid() :
            context = get_game_detail_context_data(game, self.request.user, status_form)
            return render(request, self.template_name, context)

        else:
            # get each of the GameStatus objects
            accepting_names = GameStatus.objects.get(id=1)
            in_play = GameStatus.objects.get(id=2)
            done = GameStatus.objects.get(id=3)

            # get the staged game object
            g = status_form.save(commit=False)

            # advance the staged game object's status to the next status
            if g.status == accepting_names:
                g.status = in_play
            elif g.status == in_play:
                g.status = done
            else:
                g.status = accepting_names

            # save the form and the many to many winner relationship
            status_form.save()
            status_form._save_m2m()

            return redirect(reverse_lazy('game_detail', args=[pk]))

class GameCreateView(LoginRequiredMixin, View):
    template = 'hfgame/game_form.html'
    success_url = reverse_lazy('agame_list')

    def get(self, request, pk=None) :
        form = GameCreateForm()
        context = { 'form': form }
        return render(request, self.template, context)

    def post(self, request, pk=None) :
        form = GameCreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            context = {'form' : form}
            return render(request, self.template, context)

        # Add creator and owner to the model before saving
        f = form.save(commit=False)
        f.owner = self.request.user
        f.creator = self.request.user
        f.save()
        return redirect(self.success_url)

class GameUpdateView(LoginRequiredMixin, View):
    template = 'hfgame/game_form.html'
    success_url = reverse_lazy('agame_list')

    def get(self, request, pk) :
        g = get_object_or_404(Game, id=pk, owner=self.request.user)
        form = GameUpdateForm(instance=g)
        context = { 'form': form }
        return render(request, self.template, context)

    def post(self, request, pk=None) :
        g = get_object_or_404(Game, id=pk, owner=self.request.user)
        form = GameUpdateForm(request.POST, request.FILES or None, instance=g)
        print(request.POST)

        if not form.is_valid() :
            context = {'form' : form}
            return render(request, self.template, context)

        g = form.save(commit=False)
        g.save()

        return redirect(self.success_url)

class GameDeleteView(OwnerDeleteView):
    model = Game
    template_name = "hfgame/game_delete.html"
    success_url = reverse_lazy('agame_list')

class NameCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        g = get_object_or_404(Game, id=pk)
        name_form = NameForm(request.POST)
        name = Name(text=request.POST['name'], owner=request.user, game=g)
        name.save()
        return redirect(reverse_lazy('game_detail', args=[pk]))

class NameDeleteView(OwnerDeleteView):
    model = Name
    template_name = "hfgame/name_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        game = self.object.game
        return reverse_lazy('game_detail', args=[game.id])
