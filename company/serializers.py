from api.models import User
from .models import *

from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CompanySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'password', 'profile_image','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
# Google Seri
class CompanyGoogleAuthSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'password', 'profile_image','role','is_google']
        extra_kwargs = {
            'password': {'write_only': True}
        }

# Company Creation
class CompanyInfoSerializer(ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = ['id','userId','company_name','industry','company_size','company_type','gst','description','is_verify']