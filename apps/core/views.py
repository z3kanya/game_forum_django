"""
Представления базового модуля.
"""
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserProfileSerializer, UserProfileUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes


from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET'])
def health_check(request):
    """Проверка работоспособности API."""
    return Response({'status': 'ok'})



User = get_user_model()

class RegisterView(generics.CreateAPIView):
    # Класс для регистрации пользователя

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    
    def post(self, request, *args, **kwargs):
        # метод для обработки POST-запроса

        serializer = self.get_serializer(data=request.data) # создаем сериализатор

        # обработка результата
        if serializer.is_valid():
            user = serializer.save() # вызываем метод create

            refresh = RefreshToken.for_user(user)

            return Response({
                'success': True,
                'user': UserProfileSerializer(user).data,
                'token': str(refresh.access_token), 
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # Класс для авторизации пользователя
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        # метод для обработки POST-запроса

        username = request.data.get('username')
        password = request.data.get('password')

        # проверяем, что имя пользователя и пароль были переданы
        if not username or not password:
            return Response({
                'success': False,
                'errors': 'Пожалуйста, введите имя пользователя и пароль'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # аутентификация
        user = authenticate(
            username=username,
            password=password
        )

        # обработка результата
        # if user:
        #     token, _ = Token.objects.get_or_create(user=user)

        #     return Response({
        #         'success': True,
        #         'user': UserProfileSerializer(user).data,
        #         'token': token.key
        #     })
        if user:
            refresh = RefreshToken.for_user(user) 
            return Response({
                'success': True,
                'user': UserProfileSerializer(user).data,
                'token': str(refresh.access_token),
            })
        
        return Response({
            'success': False,
            'errors': 'Неправильное имя пользователя или пароль'
        }, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    # Класс для выхода пользователя из системы

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def post(self, request):
        # метод для обработки POST-запроса

        # удаление токена
        request.user.auth_token.delete()

        return Response({
            'success': True,
            'message': 'Вы успешно вышли из системы'
        })


class ProfileView(generics.RetrieveAPIView):
    # Класс для просмотра и редактирования профиля пользователя

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # метод для получения текущего пользователя
        return self.request.user
    

class UpdateProfileView(generics.UpdateAPIView):
    # Класс для обновления профиля пользователя

    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
    pasrser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        # метод для получения текущего пользователя
        return self.request.user
    
    def perform_update(self, serializer):
        # метод для обновления профиля пользователя
        serializer.save()
    