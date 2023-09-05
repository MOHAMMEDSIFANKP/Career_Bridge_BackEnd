from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dashboard.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


# User Account 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'password', 'profile_image','role']
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
        
# User Profile
class UserProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

class IsCompletedUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['is_compleated']

def CheckuserInfo(id):
    try:
        result = UserInfo.objects.get(userId=id)
        return result.id
    except UserInfo.DoesNotExist:
        return None

class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
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

        return token

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

# Education
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

# User info
class UserInfoSerializer(serializers.ModelSerializer):
    experience = ExperienceSerializer(many=True,required=False)
    languages = LanguagesSerializers(many=True)
    jobField = JobFieldSerializers()
    jobTitle = JobTitleSerializers()
    education = EducationSerializer(many=True)
    skills = SkillsSerializers(many=True)

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
        user_info.skills.add(*Skills.objects.filter(skills__in=[skill['skills'] for skill in skills_data]))
        return user_info