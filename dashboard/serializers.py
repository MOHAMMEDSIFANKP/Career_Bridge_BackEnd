from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import JobField,JobTitle
from api.models import User

class JobFieldSerializers(ModelSerializer):
    class Meta:
        model = JobField
        fields = ['field_name']

class JobTitleSerializers(ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['title_name', 'field']


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['is_admin'] = user.is_superuser

        return token
