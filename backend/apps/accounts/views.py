from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer

# IP を変えながらの総当たりに備え、ログインID単位でも失敗回数を数えて一時ロックする
LOGIN_FAILURE_LIMIT = 10
LOGIN_LOCK_SECONDS = 15 * 60


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        return token


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

    def post(self, request, *args, **kwargs):
        login_id = str(request.data.get(get_user_model().USERNAME_FIELD, '')).strip().lower()
        failure_key = f'auth:login-failures:{login_id}'
        if cache.get(failure_key, 0) >= LOGIN_FAILURE_LIMIT:
            return Response(
                {'detail': 'ログインの失敗が続いたため、一時的にロックしています。15分ほどしてからお試しください。'},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            # 最後の失敗から LOGIN_LOCK_SECONDS 経てばリセットされる
            cache.set(failure_key, cache.get(failure_key, 0) + 1, LOGIN_LOCK_SECONDS)
            raise
        cache.delete(failure_key)
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'ログアウトしました。'})
        except Exception:
            return Response({'detail': '無効なトークンです。'}, status=400)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
