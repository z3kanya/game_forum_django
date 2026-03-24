from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Game, Genre, FavoriteGame
from .serializers import (
    GameSerializer, 
    GameShortSerializer, 
    GenreSerializer, 
    FavoriteGameSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes

class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameListShortView(generics.ListAPIView):
    serializer_class = GameShortSerializer
    def get_queryset(self):
        queryset = Game.objects.all()
        genre_id = self.request.query_params.get('genre')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        return queryset

class GameDetailView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    pagination_class = None

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_to_favorites(request, game_id):
    # Добавление игры в избранное
    game = get_object_or_404(Game, pk=game_id)

    FavoriteGame.objects.create(
        user=request.user,
        game=game
    )

    return Response({'status': 'added'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def remove_from_favorites(request, game_id):
    # Удаление игры из избранного
    game = get_object_or_404(Game, pk=game_id)

    deleted, _ = FavoriteGame.objects.filter(
        user=request.user,
        game=game
    ).delete()

    if deleted:
        return Response({'status': 'removed'})
    
    return Response(
        {'error': 'Игра не найдена в избранном'},
        status=status.HTTP_404_NOT_FOUND
    )

class FavoriteGameListView(generics.ListAPIView):
    # Список игр в избранном
    serializer_class = FavoriteGameSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        return FavoriteGame.objects.filter(user=self.request.user)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def check_favorite(request, game_id):
    # Проверка, есть ли игра в избранном
    game = get_object_or_404(Game, pk=game_id)

    is_favorite = FavoriteGame.objects.filter(
        user=request.user,
        game=game
    ).exists()

    return Response({'is_favorite': is_favorite})


class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    