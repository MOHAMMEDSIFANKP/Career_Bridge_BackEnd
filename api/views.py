from .serializers import *
from .models import User
from decouple import config
from django.db.models import Q
from .tasks import *
from company.models import *
from company.serializers import *
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView, ListCreateAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate


# Login and Token creations
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer

# Registraion for User (Include send mail)
class UserRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserSerializer
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.role = "user"
            user.set_password(password)
            user.save()
            send_activation_email.delay(email, user.pk)

            response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
                'data': serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})


# Resend Registration mail
@api_view(['POST'])
def Resend_registration_link(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email = email)
        if user:
            send_activation_email.delay(email, user.pk)
        response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
            }
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'invalid email'}, status=status.HTTP_404_NOT_FOUND)

# Email Validation link 
@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Congrats! Account activated!'
        token = create_jwt_pair_tokens(user)
        Baseurl = config('BaseUrl')
        if user.role == 'user':
           redirect_url = Baseurl + 'login' + '?message=' + message + '&token=' + str(token)
        else:
            redirect_url = Baseurl + 'login' + '?message=' + message + '&token=' + str(token)
            
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)

# Google Signup
class GoogleAuthendication(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not User.objects.filter(email=email,is_google=True).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):

                user = serializer.save()
                user.role = "user"
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()
        user = authenticate( email=email, password=password)

        if user is not None:
            token=create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registratin Successfully',
                'token': token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

def CheckuserInfo(id):
    try:
        result = UserInfo.objects.get(userId=id)
        return result.id
    except UserInfo.DoesNotExist:
        return None
# Create new token
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

# Forgot password
class Forgotpassword(APIView):
    def post(self, request):
        email =  request.data.get('email')
        if User.objects.filter(email=email).exclude(is_google=True).exists():
            user = User.objects.get(email=email)
            send_forgotpassword_email.delay(email)
            response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
                'user': user.id
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': 'Invalid Email'})


# Forgot password password changeing section
@api_view(['GET'])
def resetpassword(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    Baseurl = config('BaseUrl')
    if User.objects.filter(id=user.id).exists():
        redirect_url = Baseurl+'resetpassword'
    else:
        message = 'Invalid activation link'
        redirect_url = Baseurl+'resetpassword' + '?message=' + message
    return HttpResponseRedirect(redirect_url)

# Update User Details
class UserRestpassword(APIView):
    def put(self, request, id):
        serializer = RestPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(id=id)
                user.set_password(password)
                user.save()
                token = create_jwt_pair_tokens(user)
                response_data = {
                    'status': 'success',
                    'msg': 'Password updated successfully',
                    'token': token,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'status': 'error', 'msg': 'User not found'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Details
class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

# UserInfo list and creating
class UserInfoListCreateAPIView(ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    pagination_class = None

# User info Details
class UserInfoDetails(RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    lookup_field = 'id'

# Experiece Create and list
class ExperienceListCreateAPIView(ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = None

# Experience Details
class ExperienceDetails(RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    lookup_field = 'id'

# Education Create and list
class EducationListCreateAPIView(ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    lookup_field = 'id'

# Education Details
class EducationDetails(RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    lookup_field = 'id'

# UserInfo related Jobs Post
class UserRelatedJobs(ListAPIView):
    serializer_class = CompanyPostRetrieveSerilizer
    pagination_class = PageNumberPagination
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user_info_id = self.kwargs['id']
        user_info = UserInfo.objects.get(id=user_info_id)
        context['user_info'] = user_info 
        return context
    def get_queryset(self):
        user_info_id = self.kwargs['id']
        user_info = UserInfo.objects.get(id=user_info_id) 
        user_skills = user_info.skills.all()  
        queryset = Post.objects.filter(skills__in=user_skills,companyinfo__is_verify=True).distinct().order_by('-created_at')
        return queryset
    
# User Side Jobs Post
class UserPost(ListAPIView):
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','job_category__field_name','Jobtitle__title_name','skills__skills','work_time','level_of_experience']
    serializer_class = CompanyPostRetrieveSerilizer
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user_info_id = self.kwargs['id']
        user_info = UserInfo.objects.get(id=user_info_id)
        context['user_info'] = user_info 
        return context

    def get_queryset(self):
        skills = self.request.GET.get('skills', '')
        job_category = self.request.GET.get('job_categories', '')
        job_title = self.request.GET.get('job_title', '') 
        talent_type = self.request.GET.get('talent_type', '') 

        # Convert query parameter strings to lists
        skills_list = skills.split(',') if skills else []
        job_category_list = job_category.split(',') if job_category else []
        job_title_list = job_title.split(',') if job_title else []
        talent_type_list = talent_type.split(',') if talent_type else []
        print(talent_type_list,'daxoo')
        queryset = Post.objects.all().exclude(companyinfo__is_verify=False)

        if skills_list:
            skills_query = Q()
            for skill in skills_list:
                skills_query |= Q(skills__skills__icontains=skill)
            queryset = queryset.filter(skills_query)

        if job_category_list:
            job_category_query = Q()
            for category in job_category_list:
                job_category_query |= Q(job_category__field_name__icontains=category)
            queryset = queryset.filter(job_category_query)

        if job_title_list:
            job_title_query = Q()
            for job_title in job_title_list:
                job_title_query |= Q(Jobtitle__title_name__icontains=job_title)
            queryset = queryset.filter(job_title_query)

        if talent_type_list:
            talent_type_query = Q()
            for talent_type in talent_type_list:
                talent_type_query |= Q(level_of_experience__icontains=talent_type)
            queryset = queryset.filter(talent_type_query)

        if skills_list or job_category_list or job_title_list or talent_type_list:
            queryset = queryset.exclude(companyinfo__is_verify=False)
        queryset = queryset.distinct().order_by('-created_at')

        return queryset


# User related Apply All Job
class UserApplyPostList(ListAPIView):
    serializer_class = UserApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['comanyInfo__company_name','comanyInfo__industry','comanyInfo__userId__email','Post__job_category__field_name','Post__Jobtitle__title_name','Post__skills__skills']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(userInfo=user_info_id).order_by('-id')
    
# User related Apply Job
class UserAcceptedApplyPostList(ListAPIView):
    serializer_class = UserApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['comanyInfo__company_name','comanyInfo__industry','comanyInfo__userId__email','Post__job_category__field_name','Post__Jobtitle__title_name','Post__skills__skills']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(userInfo=user_info_id,accepted=True).order_by('-id')

# User related Apply Job
class UserPendingApplyPostList(ListAPIView):
    serializer_class = UserApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['comanyInfo__company_name','comanyInfo__industry','comanyInfo__userId__email','Post__job_category__field_name','Post__Jobtitle__title_name','Post__skills__skills']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(userInfo=user_info_id,accepted=False,rejected=False).order_by('-id')

from django.http import JsonResponse

# Notification cout
def Notification_count(request, id):
    count = Notification.objects.filter(user__id=id,is_read=False).count()
    response_data = {'count': count}
    return JsonResponse(response_data)

# Notification
class userNotification(ListAPIView):
    serializer_class = UserNotificationSerializer
    pagination_class= None
    def get_queryset(self):
        user_id = self.kwargs['id']
        if user_id:
            return Notification.objects.filter(user_id=user_id).order_by('-timestamp')
        else:
            return Notification.objects.none()

# Notification read
class NotificationRead(RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all().exclude(user__role='admin')
    serializer_class = NoficationSerializer
    lookup_field = 'id'


# Company LIst in Userside
class CompaniesList(ListAPIView):
    serializer_class = CompanyiesChattingLIst
    filter_backends = [SearchFilter]
    search_fields = ['comanyInfo__company_name']
    pagination_class = None

    def get_queryset(self):
        user_id = self.kwargs['id'] 
        return ApplyJobs.objects.filter(userInfo__userId=user_id, accepted=True).order_by('userInfo__userId', 'created_at').distinct('userInfo__userId')


