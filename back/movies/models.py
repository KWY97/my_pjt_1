from django.db import models
from django.conf import settings
import datetime

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Weather(models.Model):
    main = models.CharField(max_length=50)  # 예: Clear, Rain, Clouds, Snow

    def __str__(self):
        return self.main

class Movie(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    movie_id = models.IntegerField(primary_key=True)  # 영화의 고유 ID (TMDB에서 제공)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')  # 장르와 다대다 관계
    release_date = models.DateField(null=True, default=datetime.date.today)
    popularity = models.FloatField()
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)
    adult = models.BooleanField()
    director = models.CharField(max_length=255, null=True, blank=True)  # 감독 이름
    cast = models.TextField(null=True, blank=True)  # 출연진 이름 (쉼표로 구분된 텍스트)
    runtime = models.IntegerField(null=True, blank=True)  # 영화 상영 시간 (분 단위)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")


    def __str__(self):
        return self.title

class RecommendedMovies(models.Model):
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE, related_name='recommended_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='recommended_movies')

    def __str__(self):
        return f"{self.weather.main} - {self.movie.title}"

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="comments"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"