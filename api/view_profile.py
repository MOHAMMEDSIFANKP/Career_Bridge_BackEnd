from .serializers import *
from .models import User

# Restframework
from rest_framework.views import View
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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

# User Skill remove
@api_view(['POST'])
def remove_skill(request):
    userinfo_id = request.data.get('UserInfoId')
    skills_id = request.data.get('SkillsId')

    try:
        User_Info = UserInfo.objects.get(id=userinfo_id)
        skill_to_remove = Skills.objects.get(id=skills_id)

        User_Info.skills.remove(skill_to_remove)

        return Response({'message': 'Skill removed successfully'}, status=status.HTTP_200_OK)
    except UserInfo.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Skills.DoesNotExist:
        return Response({'message': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
    



