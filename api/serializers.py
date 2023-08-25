from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'password', 'profile_image','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Specify the User model
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile_image', 'role', 'is_google']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['is_compleated'] = user.is_compleated
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_superuser

        return token

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

# User info
class UserInfoSerializer(serializers.ModelSerializer):
    experience = ExperienceSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = '__all__'
