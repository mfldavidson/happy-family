from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from hfgame.models import *
from hfgame.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerDeleteView
from hfgame.forms import *

class AGamesListView(OwnerListView):
    model = Game
    template_name = "agame_list.html"

    def get(self, request) :
        game_list = Game.objects.filter(status='a').order_by('-updated_at').all()
        ctx = {'game_list': game_list}
        return render(request, self.template_name, ctx)

class GameDetailView(OwnerDetailView):
    model = Game
    template_name = "game_detail.html"

    def get(self, request, pk):
        game = Game.objects.get(id=pk)
        status_form = GameStatusForm()
        names = Name.objects.filter(game=game).order_by('-updated_at').all()
        name_form = NameForm()
        name_exists = Name.objects.filter(game=game, owner=self.request.user).first()
        context = {
            'game': game,
            'status_form': status_form,
            'names': names,
            'name_form': name_form,
            'name_exists': name_exists
            }
        return render(request, self.template_name, context)

class GameCreateView(LoginRequiredMixin, View):
    template = 'hfgame/game_form.html'
    success_url = reverse_lazy('agame_list')
    def get(self, request, pk=None) :
        form = GameCreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = GameCreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        f = form.save(commit=False)
        f.owner = self.request.user
        f.save()
        return redirect(self.success_url)

class GameUpdateView(LoginRequiredMixin, View):
    template = 'hfgame/game_form.html'
    success_url = reverse_lazy('agame_list')

    def get(self, request, pk) :
        g = get_object_or_404(Game, id=pk, owner=self.request.user)
        form = GameCreateForm(instance=g)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        g = get_object_or_404(Game, id=pk, owner=self.request.user)
        form = GameCreateForm(request.POST, request.FILES or None, instance=g)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        g = form.save(commit=False)
        g.save()

        return redirect(self.success_url)

class GameStatusView(LoginRequiredMixin, View):
    def post(self, request, pk=None) :
        g = get_object_or_404(Game, id=pk, owner=self.request.user)
        form = GameStatusForm(request.POST, request.FILES or None, instance=g)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, ctx)

        g = form.save()
        g.save()

        return redirect((reverse_lazy('game_detail', args=[pk])))

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
