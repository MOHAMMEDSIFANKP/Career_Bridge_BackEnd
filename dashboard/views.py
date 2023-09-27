from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,UpdateAPIView
from .models import *
from api.models import *
from rest_framework.filters import SearchFilter
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .serializers import *
# Create your views here.


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer


# Job Field Crud operations
class JobFieldListAndCreater(ListCreateAPIView):
    queryset = JobField.objects.all()
    serializer_class = JobFieldSerializers
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
    queryset = User.objects.all().exclude(is_superuser=True).order_by('-id')

# User Block Unblock
class UserBlockUnblock(UpdateAPIView):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = BlockUnblockSerializer
    lookup_field = 'id'

# Company List Sealizer
class CompanyList(ListAPIView):
    queryset = CompanyInfo.objects.all().order_by('-created_at')
    serializer_class = CompanyListSerializer

# Company Verify and Block
class VerifyAndBlock(UpdateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyVerifyBlockSerializer
    lookup_field = 'id'

# Notification
class AdminNotification(ListAPIView):
    queryset = Notification.objects.filter(user__role='admin').order_by('-timestamp')
    serializer_class = NoficationSerializer

# Notification read
class AdminNotificationRead(RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.filter(user__role='admin')
    serializer_class = NoficationSerializer
    lookup_field = 'id'

