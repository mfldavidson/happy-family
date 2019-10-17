from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

class GameStatus(models.Model):
    short = models.CharField(
            max_length=1,
            validators=[MinLengthValidator(1, 'Name must be greater than 1 character')]
            )
    long = models.CharField(
            max_length=25,
            validators=[MinLengthValidator(3, 'Name must be greater than 3 characters')]
            )

    def __repr__(self):
        return self.short

    def __str__(self):
        return self.long

class Game(models.Model):
    text = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5, 'Name must be greater than 5 characters')],
        verbose_name='Name of the Game'
        )
    descr = models.TextField(
        verbose_name='Game Description (if applicable)',
        blank=True,
        null=True
        )
    status = models.ForeignKey(
        GameStatus,
        on_delete=models.SET_DEFAULT,
        default=1
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # affiliated users
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='games_created',
        default=None,
        null=True
        )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='games_owned',
        default=None,
        null=True
        )
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='games_played'
        )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='games_won',
        default=None,
        blank=True,
        null=True
        )

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + '...'

class Name(models.Model):
    text = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(1, 'Name must be greater than 1 character')]
            )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
