from .serializers import *
from api.models import User
from .models import *

from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView,ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate


# Register for CompanyUser
class CompanyRegister(CreateAPIView):
    serializer_class = CompanySerializer  # Define the serializer class

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = self.get_serializer(data=request.data)  # Use get_serializer method
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.role = 'company'
            user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite': current_site.domain
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
                'data': serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})

# Google Register for CompanyUser
class CompanyGoogleAuthendication(APIView):
    def post(self, request):
        password = request.data.get('password')

        serializer = CompanyGoogleAuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.is_active = True
            user.is_google = True
            user.role = 'company'
            user.set_password(password)
            user.save()

            response_data = {
                'status': 'success',
                'msg': 'Registratin Successfully',
                'data': serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

# Company user Deaits for Profile
class CompanyUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'

#  Company Creations
class CompanyInfoListCreateAPIView(ListCreateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer

    def perform_create(self, serializer):
        userid = serializer.validated_data.get('userId')
        existing_company_info = CompanyInfo.objects.filter(userId=userid).first()

        if existing_company_info:
            return Response(
                {"detail": "CompanyInfo with this userid already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

# Company Deaits 
class CompanyDetails(RetrieveUpdateDestroyAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    lookup_field = 'id'

# Company Post
class CompanyPostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CompanyPost
    