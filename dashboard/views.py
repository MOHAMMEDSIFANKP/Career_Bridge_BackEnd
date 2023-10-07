from .models import *
from api.models import *
from .serializers import *
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
    queryset = JobField.objects.all().exclude(is_deleted=True)
    serializer_class = JobFieldSerializers
    pagination_class = None


    def perform_create(self, serializer):
        field_name = self.request.data.get('field_name')
        if JobField.objects.filter(field_name=field_name).exists():
            raise serializers.ValidationError("A JobField with this name already exists.")
        super().perform_create(serializer)

# List All JobCategory
class JobFieldListAndCreaterPagination(ListAPIView):
    serializer_class = JobFieldSerializers
    filter_backends = [SearchFilter]
    search_fields = ['field_name']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 8
    queryset = JobField.objects.all().exclude(is_deleted=True).order_by('-id')

# List All Deleted JobCategory
class JobFieldListDeleted(ListAPIView):
    serializer_class = JobFieldSerializers
    filter_backends = [SearchFilter]
    search_fields = ['field_name']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 8
    queryset = JobField.objects.all().exclude(is_deleted=False).order_by('-id')

class JobFieldDetails(RetrieveUpdateDestroyAPIView):
    queryset = JobField.objects.all()
    serializer_class = JobFieldSerializers
    lookup_field = 'id'

# Job Title Crud operations
class JobTitledListAndCreater(ListCreateAPIView):
    queryset = JobTitle.objects.all().exclude(is_deleted=True)
    serializer_class = JobTitleSerializers
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['title_name']

    def perform_create(self, serializer):
        title_name = self.request.data.get('title_name')
        if JobTitle.objects.filter(title_name=title_name).exists():
            raise serializers.ValidationError("A JobTitle with this name already exists.")
        super().perform_create(serializer)

class JobTitledListAndpagiantions(ListAPIView):
    queryset = JobTitle.objects.all().exclude(is_deleted=True).order_by('-id')
    serializer_class = JobTitleSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 8
    filter_backends = [SearchFilter]
    search_fields = ['title_name']

class JobTitledBlockedList(ListAPIView):
    queryset = JobTitle.objects.all().exclude(is_deleted=False).order_by('-id')
    serializer_class = JobTitleSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 8
    filter_backends = [SearchFilter]
    search_fields = ['title_name']


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

# Skills list and create
class SkillsListCreateAPIView(ListCreateAPIView):
    queryset = Skills.objects.all().exclude(is_deleted=True)
    serializer_class = SkillsSerializers
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['skills']

    def perform_create(self, serializer):
        skill = self.request.data.get('skills')
        if Skills.objects.filter(skills = skill).exists():
            raise serializers.ValidationError("A Skill with this name already exists.")
        return super().perform_create(serializer)

# All skills list
class SkillsList(ListAPIView):
    queryset = Skills.objects.all().exclude(is_deleted=True).order_by('-id')
    serializer_class = SkillsSerializers
    pagination_class = PageNumberPagination
    pagination_class.page = 8
    filter_backends = [SearchFilter]
    search_fields = ['skills']

# Blocked skills list
class BlockedSkillsList(ListAPIView):
    queryset = Skills.objects.all().exclude(is_deleted=False).order_by('-id')
    serializer_class = SkillsSerializers
    pagination_class = PageNumberPagination
    pagination_class.page = 8
    filter_backends = [SearchFilter]
    search_fields = ['skills']
    
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

from django.db.models import Sum,Count
from django.db.models.functions import ExtractMonth

@api_view(['GET'])
def get_chart_data(request):
    user_count = User.objects.filter(role='user').count()
    company_count = User.objects.filter(role='company').count()

    post_counts = Post.objects.annotate(month=ExtractMonth("created_at")).values("month").annotate(count=Count("id"))
    
    if user_count > 0 and company_count > 0 and post_counts:
        chart_data = {
            'pie_chart': {
                'labels': ["Users", "Company"],
                'datasets': [
                    {
                        'label': "Counts",
                        'data': [user_count, company_count],
                        'backgroundColor': ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                    }
                ]
            },
            'line_chart': {
                'labels': [f"Month {entry['month']}" for entry in post_counts],
                'datasets': [
                    {
                        'label': "Post Counts",
                        'data': [entry['count'] for entry in post_counts],
                        'fill': False,
                        'borderColor': "rgb(75, 192, 192)",
                        'tension': 0.1,
                    }
                ]
            }
        }
        return Response(chart_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No data available'}, status=status.HTTP_400_BAD_REQUEST)