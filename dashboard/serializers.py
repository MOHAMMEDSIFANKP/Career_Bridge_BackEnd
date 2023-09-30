from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from api.models import *
from api.serializers import *
from company.models import *
# Crud For JobList
class JobFieldSerializers(ModelSerializer):
    class Meta:
        model = JobField
        fields = ['id','field_name','is_deleted']

# Crud for Jotitle
class JobTitleSerializers(ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id','title_name', 'field','is_deleted']

# Crud for language
class LanguagesSerializers(ModelSerializer):
    class Meta:
        model = Languages
        fields = ['language']

# Crud for Skills
class SkillsSerializers(ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id','skills','is_deleted']

# Admin Authendication List
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
        exclude = ('password',)

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

# All Posts Lising
class ListAllPostSerializer(ModelSerializer):
    companyinfo = CompanyListSerializer()
    job_category = JobFieldSerializers()
    Jobtitle = JobTitleSerializers()
    skills = SkillsSerializers(many=True)
    class Meta:
        model = Post
        fields = '__all__'

# Blocked Unblock
class PostBlockUnblockserializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['is_blocked']
        
# Notification Serializer
class NoficationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
