from api.models import User
from .models import *
from dashboard.serializers import *
from django.shortcuts import get_object_or_404

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
        fields = '__all__'

# 
# Company Posts
class CompanyPost(ModelSerializer):
    job_category = JobFieldSerializers(required=False)
    Jobtitle = JobTitleSerializers(required=False)
    skills = SkillsSerializers(many=True,required=False)
    class Meta:
        model = Post
        fields= '__all__'

    def create(self, validated_data):
        job_field_name = validated_data.pop('job_category', {}).get('field_name')
        Jobtitle_data = validated_data.pop('Jobtitle', {}).get('title_name')
        companyinfo = validated_data.pop('companyinfo', None)
        skills_data = validated_data.pop('skills', [])

        post_instance = Post.objects.create(**validated_data)

        if companyinfo:
            post_instance.companyinfo = get_object_or_404(CompanyInfo, id=companyinfo.id)
            post_instance.save()
        
        if job_field_name:
            post_instance.job_category = get_object_or_404(JobField, field_name=job_field_name)

            post_instance.save()
        
        if Jobtitle_data:
            post_instance.Jobtitle = get_object_or_404(JobTitle, title_name=Jobtitle_data)
            post_instance.save()
        
        if skills_data:
            post_instance.skills.add(*Skills.objects.filter(skills__in=[skill['skills'] for skill in skills_data]),through_defaults={'set': True})
        return post_instance
