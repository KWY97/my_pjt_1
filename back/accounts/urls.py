from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('profile/<username>', ),
    path('user/', views.get_userinfo),
    path("<int:movie_id>/movies/islike/", views.movieIsLike),
]
