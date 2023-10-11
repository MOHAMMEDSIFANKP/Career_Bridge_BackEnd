from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dashboard.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
import re
from company.models import CompanyInfo
from dashboard.serializers import *
# User Account 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'password', 'profile_image','role','is_compleated']
        extra_kwargs = {
            'password': {'write_only': True}
        }

# User Google Account
class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile_image', 'role', 'is_google']
        extra_kwargs = {
            'password': {'write_only': True}
        }

def CheckuserInfo(id):
    try:
        result = UserInfo.objects.get(userId=id)
        return result.id
    except UserInfo.DoesNotExist:
        return None
def CheckcompanyInfo(id):
    try:
        result = CompanyInfo.objects.get(userId=id)
        return result.id
    except CompanyInfo.DoesNotExist:
        return None
# Token
class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.role == "user":
            userInfoId = CheckuserInfo(user.id)
            token = super().get_token(user)

            token['userInfoId']=userInfoId
            token['first_name']=user.first_name
            token['last_name'] = user.last_name
            token['email'] = user.email
            token['role'] = user.role
            token['is_compleated'] = user.is_compleated
            token['is_active'] = user.is_active
            token['is_admin'] = user.is_superuser
        else:
            companyInfoId = CheckcompanyInfo(user.id)
            token = super().get_token(user)
            token['companyInfoId'] = companyInfoId
            token['first_name']=user.first_name
            token['last_name'] = user.last_name
            token['email'] = user.email
            token['role'] = user.role
            token['is_compleated'] = user.is_compleated
            token['is_active'] = user.is_active
            token['is_admin'] = user.is_superuser
        return token

        

# Crud for Experience
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

# Crud for Education
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

# User info
class UserInfoSerializer(serializers.ModelSerializer):
    experience = ExperienceSerializer(many=True,required=False)
    languages = LanguagesSerializers(many=True,required=False)
    jobField = JobFieldSerializers(required=False)
    jobTitle = JobTitleSerializers(required=False)
    education = EducationSerializer(many=True,required=False)
    skills = SkillsSerializers(many=True,required=False)

    class Meta:
        model = UserInfo
        fields = '__all__'
        
    def create(self, validated_data):
        experience_data = validated_data.pop('experience', [])
        languages_data = validated_data.pop('languages', [])
        user_id = validated_data.pop('userId', None)
        job_field_name = validated_data.pop('jobField', {}).get('field_name')
        job_title_name = validated_data.pop('jobTitle', {}).get('title_name')
        education_data = validated_data.pop('education', [])
        skills_data = validated_data.pop('skills', [])
       
        
        if UserInfo.objects.filter(userId=user_id).exists():
            raise ValidationError('User info with this userId already exists.')

        user_info = UserInfo.objects.create(**validated_data)

        if user_id:
            user_info.userId = get_object_or_404(User, email=user_id)
            user_info.save()

        if job_field_name:
            user_info.jobField = get_object_or_404(JobField, field_name=job_field_name)
            user_info.save()

        if job_title_name:
            user_info.jobTitle = get_object_or_404(JobTitle, title_name=job_title_name)
            user_info.save()

        user_info.education.add(*[Education.objects.create(**edu) for edu in education_data])
        user_info.experience.add(*[Experience.objects.create(**exp) for exp in experience_data])
        user_info.languages.add(*[Languages.objects.get_or_create(language=lang['language'])[0] for lang in languages_data])
        user_info.skills.add(*Skills.objects.filter(skills__in=[skill['skills'] for skill in skills_data]),through_defaults={'set': True})

        return user_info
    
    def update(self, instance, validated_data):
        job_field_name = validated_data.pop('jobField', {}).get('field_name')
        job_title_name = validated_data.pop('jobTitle', {}).get('title_name')
        bio = validated_data.pop('bio', None)
        skills_data = validated_data.pop('skills', [])
        cv = validated_data.pop('cv', None)
        experience_data = validated_data.pop('experience', [])
        education_data = validated_data.pop('education', [])
        streetaddress = validated_data.pop('streetaddress', None)
        city = validated_data.pop('city', None)
        state = validated_data.pop('state', None)
        zipcode = validated_data.pop('zipcode', None)

        # experience_data = validated_data.pop

        if job_field_name and job_title_name:
            instance.jobField = JobField.objects.get(field_name=job_field_name)
            instance.jobTitle = JobTitle.objects.get(title_name=job_title_name)
            instance.save()

        if bio:
            instance.bio = bio
            instance.save()

        if skills_data:
            new_skills = [skill['skills'] for skill in skills_data]
            skills_to_add = Skills.objects.filter(skills__in=new_skills)
            instance.skills.add(*skills_to_add, through_defaults={'set': True})

        if cv:
            instance.cv = cv
            instance.save()
        
        if experience_data:
            instance.experience.add(*[Experience.objects.create(**exp) for exp in experience_data])

        if education_data:
           instance.education.add(*[Education.objects.create(**edu) for edu in education_data])

        if streetaddress and city and state and zipcode:
            instance.streetaddress = streetaddress
            instance.city = city
            instance.state = state
            instance.zipcode = zipcode
            instance.save()

        return instance



#--------------------------------UPDATE----------------------------------------------# 

# Rest password
class RestPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

# Update User Profile
class UserProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

# Update is compleated
class IsCompletedUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['is_compleated']
        
# Update User Details (First_name, Last_name, Email)
class UpdateUseAccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name']

from django.utils import timezone
# ApplyJob in UserSide
class UserApplyJobSListerializer(ModelSerializer):
    Post = ListAllPostSerializer()
    days = serializers.SerializerMethodField()
    class Meta:
        model = ApplyJobs
        fields = '__all__'

    def get_days(self, obj):
        now = timezone.now()
        delta = now - obj.created_at
        return delta.days

# User Notification
class UserNotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# CompanyList
class CompanyiesChattingLIst(ModelSerializer):
    userId = serializers.IntegerField(source='comanyInfo.userId.id', read_only=True)
    email = serializers.CharField(source='comanyInfo.userId.email', read_only=True)
    company_name = serializers.CharField(source='comanyInfo.company_name', read_only=True)
    profile_image = serializers.ImageField(source='comanyInfo.userId.profile_image', read_only=True)
    class Meta:
        model = ApplyJobs
        fields = ['userId','email','company_name','profile_image']

