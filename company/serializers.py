from api.models import User
from .models import *
from dashboard.serializers import *
from api.serializers import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone


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
        fields = '__all__'


# Company Posts
class CompanyPost(ModelSerializer):
    class Meta:
        model = Post
        fields= '__all__'

# Company Posts getting
class CompanyPostRetrieveSerilizer(ModelSerializer):
    companyinfo = CompanyInfoSerializer(required=False)
    job_category = JobFieldSerializers(required=False)
    Jobtitle = JobTitleSerializers(required=False)
    skills = SkillsSerializers(many=True,required=False)
    days = serializers.SerializerMethodField()
    applied = serializers.SerializerMethodField()
    user_profile = UserProfileUpdateSerializer(source='companyinfo.userId', read_only=True)
    class Meta:
        model = Post
        fields= '__all__'

    def get_days(self, obj):
        now = timezone.now()
        delta = now - obj.created_at
        return delta.days
    def get_applied(self, obj):
        user_info = self.context.get('user_info')  
        if user_info:
            if ApplyJobs.objects.filter(userInfo=user_info, Post_id=obj.id).exists():
                return True
            else:
                return False
        else:
            return False 



# Company Posts Block unblok and Delete un delete
class CompanyPostBlockUnblock(ModelSerializer):
    class Meta:
        model = Post
        fields= ['is_blocked','is_deleted']

# User Apply for the job
class ApplyJobSerializer(ModelSerializer):
    class Meta:
        model = ApplyJobs
        fields = '__all__'

class ApplyJobSListerializer(ModelSerializer):
    userInfo = UserInfoSerializer()
    Post = ListAllPostSerializer()
    days = serializers.SerializerMethodField()
    user = UserSerializer(source='userInfo.userId', read_only=True)
    class Meta:
        model = ApplyJobs
        fields = '__all__'

    def get_days(self, obj):
        now = timezone.now()
        delta = now - obj.created_at
        return delta.days
    
# Accept or rejected
class Accept_or_rejected_ApplyJobsSerializer(ModelSerializer):
    class Meta:
        model = ApplyJobs
        fields = ['accepted','rejected']

class ScheduleDateSerializers(ModelSerializer):
    class Meta:
        model = ApplyJobs
        fields = ['schedule']

class CompanyNotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class UserInfoListSerializer(ModelSerializer):
    userId = UsersListSerializer()
    skills = SkillsSerializers(many=True)
    jobField = JobFieldSerializers()
    jobTitle = JobTitleSerializers()
    experience = ExperienceSerializer(many=True)
    languages = LanguagesSerializers(many=True)
    education = EducationSerializer(many=True)
    class Meta:
        model = UserInfo
        fields = '__all__'


# CompanyList
class UsersChatListSerializer(ModelSerializer):
    userId = serializers.IntegerField(source='userInfo.userId.id', read_only=True)
    email = serializers.CharField(source='userInfo.userId.email', read_only=True)
    first_name = serializers.CharField(source='userInfo.userId.first_name', read_only=True)
    last_name = serializers.CharField(source='userInfo.userId.last_name', read_only=True)
    profile_image = serializers.ImageField(source='userInfo.userId.profile_image', read_only=True)
    class Meta:
        model = ApplyJobs
        fields = ['userId','email','first_name','last_name','profile_image']

# Invite Users
class UserInveiteSerializer(ModelSerializer):
    class Meta:
        model = InviteUsers
        fields = '__all__'

# Invite User shows in userside
class InviteUserListUsersides(ModelSerializer):
    comanyInfo = CompanyInfoSerializer()
    Post = ListAllPostSerializer()
    days = serializers.SerializerMethodField()
    class Meta:
        model = InviteUsers
        fields = '__all__'

    def get_days(self, obj):
        now = timezone.now()
        delta = now - obj.created_at
        return delta.days
    
# Company side Users lisitng
class UserlistCompanyserializer(ModelSerializer):
    invited = serializers.SerializerMethodField()
    jobField = JobFieldSerializers()
    jobTitle = JobTitleSerializers()
    userId = UserSerializer()
    experience = ExperienceSerializer(many=True)
    languages = LanguagesSerializers(many=True)
    education = EducationSerializer(many=True)
    skills = SkillsSerializers(many=True)
    class Meta:
        model = UserInfo
        fields = '__all__'
    def get_invited(self, obj):
        comapny_info = self.context.get('comapny_info')  
        if comapny_info:
            if InviteUsers.objects.filter(comanyInfo=comapny_info, userInfo=obj.id).exists():
                return True
            else:
                return False
        else:
            return False 
        
# Unkown users Home page
class UnkownUserSerializer(ModelSerializer):
    days = serializers.SerializerMethodField()
    companyinfo = CompanyInfoSerializer()
    job_category = JobFieldSerializers()
    Jobtitle = JobTitleSerializers()
    skills = SkillsSerializers(many=True)
    profile_image = serializers.ImageField(source='companyinfo.userId.profile_image', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
    def get_days(self, obj):
        now = timezone.now()
        delta = now - obj.created_at
        return delta.days