from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from movies.models import Movie

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 로그인된 사용자만 접근 가능
def get_userinfo(request):
    user = request.user  # 현재 요청을 보낸 사용자 객체
    data = {
        "username": user.username,
        "email": user.email,
        "id": user.id,  # 필요에 따라 추가 가능
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movieIsLike(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user.like_movies.filter(pk=movie_id).exists():
        return Response({'is_Liked': True})
    else:
        return Response({'is_liked': False})