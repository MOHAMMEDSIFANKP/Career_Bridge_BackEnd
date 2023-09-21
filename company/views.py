from .serializers import *
from api.models import User
from .models import *
from django.shortcuts import render
from api.tasks import *

from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView,ListCreateAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

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
            send_activation_email.delay(email, user.pk)

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
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = CompanyGoogleAuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.is_active = True
            user.is_google = True
            user.role = 'company'
            user.set_password(password)
            user.save()
        user = authenticate( email=email, password=password)
        if user is not None:
            token=create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registratin Successfully',
                'token': token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

def CheckcompanyInfo(id):
    try:
        result = CompanyInfo.objects.get(userId=id)
        return result.id
    except CompanyInfo.DoesNotExist:
        return None
    
def create_jwt_pair_tokens(user):
    companyInfoId = CheckcompanyInfo(user.id)
    
    refresh = RefreshToken.for_user(user)
    refresh['companyInfoId'] = companyInfoId
    refresh['first_name']=user.first_name
    refresh['last_name'] = user.last_name
    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh['is_compleated'] = user.is_compleated
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser

    access_token = str(refresh.access_token) 
    refresh_token = str(refresh)
    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }
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

# Company Deaits 
class CompanyPostDetails(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = CompanyPostRetrieveSerilizer
    lookup_field = 'id'

# Companyside Post listing 
class Listofcompanypost(ListAPIView):
    serializer_class = CompanyPostRetrieveSerilizer
    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return Post.objects.filter(companyinfo_id=company_info_id)

def seeimages(request):
    return render (request, 'company/email_template.html')