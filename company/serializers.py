from api.models import User
from .models import *
from dashboard.serializers import *
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
    class Meta:
        model = Post
        fields= '__all__'

# Company Posts Block unblok and Delete un delete
class CompanyPostBlockUnblock(ModelSerializer):
    class Meta:
        model = Post
        fields= ['is_blocked','is_deleted']
