from .serializers import *
from .models import User
from django.contrib.auth.hashers import check_password

# Restframework
from rest_framework.views import View
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Profile image update
class UserProfileUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    lookup_field = 'id'
# Update is Compleated
class Is_compleatedUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = IsCompletedUpdateSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        response = super(Is_compleatedUpdate, self).update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = self.get_object()
            user.is_compleated = True
            user.save()
            refresh = create_jwt_pair_tokens(user)
            serialized_user = IsCompletedUpdateSerializer(user)
            return Response({
                'token': str(refresh),
                'user': serialized_user.data
            }, status=status.HTTP_200_OK)

        return response 
    
def CheckuserInfo(id):
    try:
        result = UserInfo.objects.get(userId=id)
        return result.id
    except UserInfo.DoesNotExist:
        return None
    
def create_jwt_pair_tokens(user):
    userInfoId = CheckuserInfo(user.id)
    
    refresh = RefreshToken.for_user(user)
    refresh['userInfoId'] = userInfoId
    refresh['first_name'] = user.first_name
    refresh['last_name'] = user.last_name
    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh['is_compleated'] = user.is_compleated
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser

    access_token = str(refresh.access_token) # type: ignore
    refresh_token = str(refresh)

    return {
        "access": access_token,
        "refresh": refresh_token,
    }


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

# Reset Password
@api_view(['POST'])
def reset_password(request,id):
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    try:
        user = User.objects.get(id=id)
        if check_password(old_password, user.password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'Password did not match'},status=status.HTTP_400_BAD_REQUEST)

        return Response({'message' : 'Wrong old password'},status=status.HTTP_400_BAD_REQUEST)
            
    except User.DoesNotExist:
        return Response ({'message' : 'user Not found'},status=status.HTTP_400_BAD_REQUEST)


