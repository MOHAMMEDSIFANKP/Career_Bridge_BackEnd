from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from api.models import *
from api.serializers import *
from company.models import *
class JobFieldSerializers(ModelSerializer):
    class Meta:
        model = JobField
        fields = ['id','field_name']

class JobTitleSerializers(ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id','title_name', 'field']


class LanguagesSerializers(ModelSerializer):
    class Meta:
        model = Languages
        fields = ['language']

class SkillsSerializers(ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id','skills']

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['role'] = user.role
        token['is_admin'] = user.is_superuser

        return token

# UserList Serializer
class UsersListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Block UnBlock Serializer
class BlockUnblockSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']

# CompanyLIst Serializer
class CompanyListSerializer(ModelSerializer):
    userId = UsersListSerializer()
    class Meta:
        model = CompanyInfo
        fields = '__all__'

# Company Verify Block Serializer
class CompanyVerifyBlockSerializer(ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = ['is_verify']

# Notification Serializer
class NoficationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'