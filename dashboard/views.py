from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import *
from rest_framework.filters import SearchFilter
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .serializers import JobFieldSerializers,JobTitleSerializers,AdminTokenObtainPairSerializer,LanguagesSerializers
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