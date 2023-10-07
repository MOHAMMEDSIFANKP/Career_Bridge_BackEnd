from django.shortcuts import render
from .serializers import *
from company.models import ApplyJobs

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView,ListAPIView


class ChatCreatingView(CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

