from .serializers import UserSerializer,myTokenObtainPairSerializer
from .models import User
from .email import send_verification_email

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import HttpResponseRedirect

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer

class UserRegister(CreateAPIView):
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(self.request, user)

@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Congrats! Account activated!'
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)

class UserList(ListCreateAPIView):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']

class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
