from django.conf import settings
from django.contrib.auth import login, logout

from rest_framework import generics, permissions, response, status, views
from rest_framework.response import Response

from core.serializers import (
    RegisterSerializer, SMSLoginSerializer, SMSSendCodeSerializer,
    UserSerializer
)


class SMSSendCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SMSSendCodeSerializer(data=request.data)
        if serializer.is_valid():
            res = {'message': 'Success'}
            if settings.DEBUG:
                res.update({'code': serializer.validated_data.get('phone')})
            return Response(res)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SMSLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return response.Response()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_object(self, *args, **kwargs):
        return self.request.user
