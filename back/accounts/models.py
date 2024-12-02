from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie

class User(AbstractUser):
    favorite_movies = models.ManyToManyField(Movie, related_name='favorite_user')
    followings = models.ManyToManyField("self", symmetrical=False, related_name='followers')