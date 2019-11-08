from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.AGamesListView.as_view(), name='agame_list' ),
    path('how-to-play/', views.HowToPlayView.as_view(), name='how_to_play'),
    path('how-to-play/original_game', views.OriginalGameView.as_view(), name='original_game'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('game/create/', views.GameCreateView.as_view(), name='game_create'),
    path('game/<int:pk>/update/', views.GameUpdateView.as_view(), name='game_update'),
    path('game/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('game/<int:pk>/name/', views.NameCreateView.as_view(), name='name_create'),
    path('name/<int:pk>/delete/', views.NameDeleteView.as_view(success_url=reverse_lazy('agame_list')), name='name_delete'),
]
