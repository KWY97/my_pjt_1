from rest_framework import serializers
from .models import Movie, Comment, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class MovieListSerializer(serializers.ModelSerializer):
  genres = GenreSerializer(read_only=True, many=True)
  # like_users_count = serializers.IntegerField(source="like_users.count", read_only=True)

  class Meta:
    model = Movie
    fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # 유저의 username만 표시
    movie_title = serializers.CharField(source="movie.title", read_only=True)  # 영화 제목 표시

    class Meta:
        model = Comment
        fields = ('id', 'user', 'movie_title', 'content', 'created_at')  # 필요한 필드만 지정
        read_only_fields = ('id', 'user', 'movie_title', 'created_at', 'movie')  # 읽기 전용 필드

class MovieSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"
  
