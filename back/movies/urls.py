from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movies_list), # 로그인 후 메인 페이지
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/likes/', views.movie_likes),
    path('recommend/<str:city>/', views.get_weather_based_recommendations, name='weather_based_recommendations'),  # 날씨 기반 영화 추천
    path('top/', views.get_top_movies, name='top_movies'),
    path('latest_anime/', views.get_latest_anime, name='latest_anime'),
    path('top_adult/', views.get_top_adult_movies, name='top_adult_movies'),
    path('<int:movie_id>/comments/', views.movie_comments, name='movie_comments'), 
    path('<int:movie_id>/comments/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    path('search/<str:keyWord>/', views.do_search),
    path('genres/', views.genre_list),
    path('genre/<str:genre>/', views.get_movies_by_genre),
    path('users/<int:user_id>/movies/<int:movie_id>/isliked/', views.is_movie_liked), # 특정 영화에 대한 좋아요 여부
    path('users/<int:user_id>/liked-movies/', views.user_liked_movies), # 좋아요한 영화 리스트
]
