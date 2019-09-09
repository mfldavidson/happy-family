from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

class Game(models.Model):
    # choices for status
    STATUS_CHOICES = [
    ('a', 'Accepting Names'),
    ('p', 'In Play'),
    ('d', 'Done')
    ]

    # model fields
    text = models.CharField(
            max_length=100,
            validators=[MinLengthValidator(5, 'Name must be greater than 5 characters')],
            verbose_name='Name of the Game'
        )
    descr = models.TextField(
        verbose_name='Game Description (if applicable)',
        null=True
        )
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='a',
        max_length=25
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # affiliated users
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='games_owned'
        )
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='games_played'
        )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
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
