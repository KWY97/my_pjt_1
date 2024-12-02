from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Movie, Comment, Genre
from .serializers import MovieListSerializer, MovieSerializer, CommentSerializer, MovieSearchSerializer, GenreSerializer
from django.db.models import Q
from accounts.models import User

import requests

API_KEY = 'Input Your API KEY' # 본인의 API 키 입력하기
BASE_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'


@api_view(['GET'])
def get_top_movies(request):
    # 인기순으로 영화 10개 가져오기
    movies = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
    }
    response = requests.get(BASE_WEATHER_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather_based_recommendations(request, city):
    current_city = city
    # 1. OpenWeatherMap API에서 부산의 날씨 정보를 가져옴
    weather_data = get_weather_data(current_city)
    if not weather_data:
        return Response({"error": "날씨 정보를 가져오는 데 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 2. 날씨 정보에서 main 값을 가져옴
    weather_main = weather_data['weather'][0]['main']

    # 3. 날씨에 따라 추천할 장르 선택
    genre_pks = []
    if weather_main == "Clear":
        genre_pks = [35]  # 코미디
    elif weather_main in ["Clouds", "Mist", "Haze", "Fog"]:
        genre_pks = [9648, 14]  # 미스터리, 판타지
    elif weather_main == "Snow":
        genre_pks = [16]  # 애니메이션
    elif weather_main in ["Rain", "Drizzle"]:
        genre_pks = [10749]  # 로맨스
    elif weather_main in ["Thunderstorm", "Ash", "Squall", "Tornado"]:
        genre_pks = [53]  # 스릴러
    elif weather_main in ["Dust", "Sand"]:
        genre_pks = [10752]  # 전쟁

    # 4. 선택한 장르에 속하는 영화 중에서 인기순으로 최대 20개 가져옴
    movies = Movie.objects.filter(genres__pk__in=genre_pks).order_by('-popularity')[:20]

    # 5. 시리얼라이저를 통해 응답 데이터 생성
    serializer = MovieListSerializer(movies, many=True)

    # 6. 날씨 정보와 영화 목록을 함께 반환
    return Response({
        "movies": serializer.data,
        "weather_main": weather_main,
        "city_name": weather_data['name'],
    })


@api_view(['GET'])
def get_latest_anime(request):
    # 애니메이션 장르 (pk=16)를 필터링하여 출시일 기준으로 최신 10개 가져옴
    latest_anime = Movie.objects.filter(genres__pk=16).order_by('-release_date')[:10]
    serializer = MovieListSerializer(latest_anime, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_top_adult_movies(request):
    top_adult_movies = Movie.objects.filter(adult=True).order_by('-popularity')
    serializer = MovieListSerializer(top_adult_movies, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movies_list(request):
    if request.method == 'GET':
        # movies = Movie.objects.all()
        movies = Movie.objects.all().order_by('-popularity')[:525]
        paginator = PageNumberPagination()
        paginator.page_size = 35  # 한 페이지에 표시할 영화 수 설정

        # 페이지네이션을 적용한 결과 가져오기
        result_page = paginator.paginate_queryset(movies, request)
        serializer = MovieListSerializer(result_page, many=True)

        # 페이지네이션된 응답 반환
        return paginator.get_paginated_response(serializer.data)

    # 페이지 넘기기 버튼, POST 요청입니다. 
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save(user=request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_comments(request, movie_id):
    # 댓글 조회
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_id)
        comment = Comment.objects.filter(movie=movie).order_by('-created_at')  # 최신 순 정렬
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    # 댓글 생성
    elif request.method == 'POST':
        movie = Movie.objects.get(pk=movie_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)  # 유저와 영화 정보 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, movie_id, comment_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    comment = get_object_or_404(Comment, pk=comment_id, movie=movie)

    # 요청한 유저와 댓글 작성자가 일치하는지 확인
    if request.user != comment.user:
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        # 댓글 수정
        serializer = CommentSerializer(comment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # 댓글 삭제
        comment.delete()
        return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def do_search(request, keyWord):
    key_list = list(keyWord.split())

    the_movie = Movie.objects.filter(title=keyWord)

    search_result = set()
    for key in key_list:
        movies = Movie.objects.filter(Q(title__icontains=key))
                                      
        for movie in movies:
            if movie not in the_movie:
                search_result.add(movie)
    
    serializer = MovieSearchSerializer(search_result, many=True)

    if the_movie:
        the_movie_serializer = MovieSearchSerializer(the_movie[0])
        return Response({"the_movie_serializer" : the_movie_serializer.data, "serializer" : serializer.data})
    else:
        return Response({"the_movie_serializer" : "", "serializer" : serializer.data})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genre_list(request):
    genres = get_list_or_404(Genre)
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_movies_by_genre(request, genre):
    try:
        # 장르 이름으로 장르 객체 가져오기
        genre_obj = Genre.objects.get(name=genre)
    except Genre.DoesNotExist:
        # 장르가 없는 경우 404 응답 반환
        return Response({"error": "Genre not found."}, status=404)

    if request.method == 'GET':
        # GET 요청: 해당 장르의 영화 목록 반환
        movies = genre_obj.movies.all().order_by('-popularity')  # 인기순 정렬
        paginator = PageNumberPagination()
        paginator.page_size = 35  # 한 페이지에 표시할 영화 수 설정

        # 페이지네이션을 적용한 결과 가져오기
        result_page = paginator.paginate_queryset(movies, request)
        serializer = MovieListSerializer(result_page, many=True)

        # 페이지네이션된 응답 반환
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        # POST 요청: 해당 장르에 새로운 영화 추가
        data = request.data
        data['genres'] = [genre_obj.id]  # POST 요청 데이터에 해당 장르 추가
        serializer = MovieSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # 새 영화 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if movie.like_users.filter(pk=request.user.id).exists():
        movie.like_users.remove(request.user)
        is_liked = False
    else:
        movie.like_users.add(request.user)
        is_liked = True

    return Response({"is_liked": is_liked}, status=status.HTTP_200_OK)


# 좋아요한 전체 영화보기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_liked_movies(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    liked_movies = user.like_movies.all()  # 유저가 좋아요를 누른 영화 리스트

    # 필요한 필드를 반환하도록 직렬화
    serializer = MovieListSerializer(liked_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 개별영화의 좋아요 여부
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_movie_liked(request, user_id, movie_id):
    user = get_object_or_404(User, pk=user_id)
    movie = get_object_or_404(Movie, pk=movie_id)

    is_liked = user.like_movies.filter(pk=movie.pk).exists()  # 좋아요 여부 확인
    return Response({'is_liked': is_liked}, status=status.HTTP_200_OK)


