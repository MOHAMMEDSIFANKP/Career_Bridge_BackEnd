from rest_framework.views import View
from rest_framework.generics import UpdateAPIView
from .serializers import *
from .models import User

class UserProfileUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    lookup_field = 'id'

class Is_compleatedUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = IsCompletedUpdateSerializer
    lookup_field = 'id'

class UpdateUseAccount(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUseAccountSerializer
    lookup_field = 'id'

    

