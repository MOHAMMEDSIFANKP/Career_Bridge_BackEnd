from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class JobFieldSerializers(ModelSerializer):
    class Meta:
        model = JobField
        fields = ['id','field_name']

class JobTitleSerializers(ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['title_name', 'field']


class LanguagesSerializers(ModelSerializer):
    class Meta:
        model = Languages
        fields = ['language']

class SkillsSerializers(ModelSerializer):
    class Meta:
        model = Skills
        fields = ['skills']

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['role'] = user.role
        token['is_admin'] = user.is_superuser

        return token
