from .models import *
from api.models import *
from .serializers import *
from django.core.exceptions import ValidationError

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,UpdateAPIView
from rest_framework.filters import SearchFilter
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer


# Job Field Crud operations
class JobFieldListAndCreater(ListCreateAPIView):
    queryset = JobField.objects.all()
    serializer_class = JobFieldSerializers
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['field_name']

    def perform_create(self, serializer):
        field_name = self.request.data.get('field_name')
        if JobField.objects.filter(field_name=field_name).exists():
            raise serializers.ValidationError("A JobField with this name already exists.")
        super().perform_create(serializer)

class JobFieldDetails(RetrieveUpdateDestroyAPIView):
    queryset = JobField.objects.all()
    serializer_class = JobFieldSerializers
    lookup_field = 'id'

# Job Title Crud operations
class JobTitledListAndCreater(ListCreateAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializers
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['title_name']

    def perform_create(self, serializer):
        title_name = self.request.data.get('title_name')
        if JobTitle.objects.filter(title_name=title_name).exists():
            raise serializers.ValidationError("A JobTitle with this name already exists.")
        super().perform_create(serializer)

class JobTitledDetails(RetrieveUpdateDestroyAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializers
    lookup_field = 'id'


class LanguageListCreateAPIView(ListCreateAPIView):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializers
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['language']

    def perform_create(self, serializer):
        language = self.request.data.get('language')
        if Languages.objects.filter(language=language).exists():
            raise serializers.ValidationError("A language with this name already exists.")
        super().perform_create(serializer)

class LanguagesdDetails(RetrieveUpdateDestroyAPIView):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializers
    lookup_field = 'id'

class SkillsListCreateAPIView(ListCreateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializers
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['skills']

    def perform_create(self, serializer):
        skill = self.request.data.get('skills')
        if Skills.objects.filter(skills = skill).exists():
            raise serializers.ValidationError("A Skill with this name already exists.")
        return super().perform_create(serializer)
    
class SkillsDetails(RetrieveUpdateDestroyAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializers
    lookup_field = 'id'

# User List
class UsersList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email','first_name','last_name','role']
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(role='user').exclude(is_superuser=True).order_by('-id')

# Comapny User List
class CompanyUsersList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email','first_name','last_name','role']
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(role='company').exclude(is_superuser=True).order_by('-id')

# Bloc User List
class BlockUsersList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email','first_name','last_name','role']
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(role='user',is_active=False).exclude(is_superuser=True).order_by('-id')

# Bloc Comany User List
class BlockCompanyUserList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email','first_name','last_name','role']
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(role='company',is_active=False).exclude(is_superuser=True).order_by('-id')

# User Block Unblock
class UserBlockUnblock(UpdateAPIView):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = BlockUnblockSerializer
    lookup_field = 'id'

# All Company List
class CompanyList(ListAPIView):
    serializer_class = CompanyListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['company_name','industry','company_type','gst','country','state','city','zipcode','userId__email']
    pagination_class = PageNumberPagination
    queryset = CompanyInfo.objects.all().order_by('-created_at')

# All Company Verified List
class CompanyVerifiedList(ListAPIView):
    serializer_class = CompanyListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['company_name','industry','company_type','gst','country','state','city','zipcode','userId__email']
    pagination_class = PageNumberPagination
    queryset = CompanyInfo.objects.filter(is_verify=True).order_by('-created_at')

# All Company Blocked List
class CompanyBlockedList(ListAPIView):
    serializer_class = CompanyListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['company_name','industry','company_type','gst','country','state','city','zipcode','userId__email']
    pagination_class = PageNumberPagination
    queryset = CompanyInfo.objects.filter(is_verify=False).order_by('-created_at')


# Company Verify and Block
class VerifyAndBlock(UpdateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyVerifyBlockSerializer
    lookup_field = 'id'

# List All Post
class ListAllPost(ListAPIView):
    serializer_class = ListAllPostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','companyinfo__userId__email','job_category__field_name','Jobtitle__title_name','skills__skills','work_time','level_of_experience']
    pagination_class = PageNumberPagination
    queryset = Post.objects.all().exclude(companyinfo__is_verify=False)

# List All Post
class ListBlockPost(ListAPIView):
    serializer_class = ListAllPostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','companyinfo__userId__email','job_category__field_name','Jobtitle__title_name','skills__skills','work_time','level_of_experience']
    pagination_class = PageNumberPagination
    queryset = Post.objects.filter(is_blocked=True).exclude(companyinfo__is_verify=False)


# Post Blocked Unblocked
class PostBlockedUnblocked(UpdateAPIView):
    serializer_class = PostBlockUnblockserializer
    queryset = Post.objects.all().exclude(companyinfo__is_verify=False)
    lookup_field = 'id'
# Notification
class AdminNotification(ListAPIView):
    queryset = Notification.objects.filter(user__role='admin').order_by('-timestamp')
    serializer_class = NoficationSerializer
    pagination_class = None

# Notification read
class AdminNotificationRead(RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.filter(user__role='admin')
    serializer_class = NoficationSerializer
    lookup_field = 'id'

