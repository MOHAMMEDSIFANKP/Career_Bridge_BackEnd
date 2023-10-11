from .serializers import *
from api.models import User
from .models import *
from django.shortcuts import render
from api.tasks import *
from .tasks import *
from django.db.models import Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView,ListCreateAPIView,ListAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate


# Register for CompanyUser
class CompanyRegister(CreateAPIView):
    serializer_class = CompanySerializer  # Define the serializer class

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = self.get_serializer(data=request.data)  # Use get_serializer method
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.role = 'company'
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

# Google Register for CompanyUser
class CompanyGoogleAuthendication(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = CompanyGoogleAuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.is_active = True
            user.is_google = True
            user.role = 'company'
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

def CheckcompanyInfo(id):
    try:
        result = CompanyInfo.objects.get(userId=id)
        return result.id
    except CompanyInfo.DoesNotExist:
        return None
    
def create_jwt_pair_tokens(user):
    companyInfoId = CheckcompanyInfo(user.id)
    
    refresh = RefreshToken.for_user(user)
    refresh['companyInfoId'] = companyInfoId
    refresh['first_name']=user.first_name
    refresh['last_name'] = user.last_name
    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh['is_compleated'] = user.is_compleated
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser

    access_token = str(refresh.access_token) 
    refresh_token = str(refresh)
    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }
# Company user Deaits for Profile
class CompanyUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'

#  Company Creations
class CompanyInfoListCreateAPIView(ListCreateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    pagination_class = None

    def perform_create(self, serializer):
        userid = serializer.validated_data.get('userId')
        existing_company_info = CompanyInfo.objects.filter(userId=userid).first()
        recipients = User.objects.filter(is_superuser=True)
        company_name = serializer.validated_data.get('company_name')
        message = f'New Company "{company_name}" is Registered, Please verify'
        path = 'Company'
        for recipient in recipients:
            Notification.objects.create(user=recipient,message=message, path=path)
        if existing_company_info:
            return Response(
                {"detail": "CompanyInfo with this userid already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

# Company Deaits 
class CompanyDetails(RetrieveUpdateDestroyAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    lookup_field = 'id'

# Company Post
class CompanyPostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CompanyPost
    pagination_class = None

# Company Post Updation
class CompanyPostUpdate(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = CompanyPost
    lookup_field = 'id'

# Company Deaits 
class CompanyPostDetails(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = CompanyPostRetrieveSerilizer
    lookup_field = 'id'

# Company Post Updation
class CompanyPostBolckUnblock(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = CompanyPostBlockUnblock
    lookup_field = 'id'

# Companyside Post listing 
class Listofcompanypost(ListAPIView):
    serializer_class = CompanyPostRetrieveSerilizer
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','job_category__field_name','Jobtitle__title_name','skills__skills','work_time','level_of_experience']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return Post.objects.filter(companyinfo_id=company_info_id,is_blocked=False,is_deleted=False).order_by('-created_at')

# Companyside Post listing 
class ListofcompanypostArchived(ListAPIView):
    serializer_class = CompanyPostRetrieveSerilizer
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','job_category__field_name','Jobtitle__title_name','skills__skills','work_time','level_of_experience']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return Post.objects.filter(companyinfo_id=company_info_id,is_deleted=True).order_by('-created_at')

# Companyside Post listing 
class ListofcompanypostBlocked(ListAPIView):
    serializer_class = CompanyPostRetrieveSerilizer
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','job_category__field_name','Jobtitle__title_name','skills__skills','work_time','level_of_experience']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return Post.objects.filter(companyinfo_id=company_info_id,is_blocked=True).order_by('-created_at')


# User Apply for the Job
class ApplyJobsCreation(CreateAPIView):
    queryset = ApplyJobs.objects.all()
    serializer_class = ApplyJobSerializer

    def perform_create(self, serializer):
        user_info = serializer.validated_data.get('userInfo')
        post = serializer.validated_data.get('Post')

        if ApplyJobs.objects.filter(userInfo=user_info.id, Post=post.id).exists():
            return Response(
                {"error": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        job_name = post.Jobtitle.title_name
        company_id = post.companyinfo.userId
        user_id = user_info.userId

        if company_id:
            message = f'{user_id.first_name} {user_id.last_name} applied for the position "{job_name}"'
            path = '/company/dashboard/'
            Notification.objects.create(user=company_id, message=message, path=path)

        if user_id:
            message = f'Congratulations, {user_id.first_name} {user_id.last_name}! You have successfully applied for the "{job_name}" position.'
            path = '/user/dashboard/'
            Notification.objects.create(user=user_id, message=message, path=path)

# Apply jobs List
class CompanyApplyPostList(ListAPIView):
    serializer_class = ApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['userInfo__userId__email','userInfo__userId__first_name','userInfo__userId__last_name']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(comanyInfo=company_info_id).order_by('-id')

# Apply jobs Pending List
class Pending_ApplyJob(ListAPIView):
    serializer_class = ApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['userInfo__userId__email','userInfo__userId__first_name','userInfo__userId__last_name']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(comanyInfo=company_info_id,accepted=False,rejected=False).order_by('-id')

# Apply jobs Accepted List
class Accepted_ApplyJob(ListAPIView):
    serializer_class = ApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['userInfo__userId__email','userInfo__userId__first_name','userInfo__userId__last_name']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(comanyInfo=company_info_id,accepted=True).order_by('-id')

# Apply jobs Rejected List
class Rejected_ApplyJob(ListAPIView):
    serializer_class = ApplyJobSListerializer
    filter_backends = [SearchFilter]
    search_fields = ['userInfo__userId__email','userInfo__userId__first_name','userInfo__userId__last_name']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        company_info_id = self.kwargs['id']
        return ApplyJobs.objects.filter(comanyInfo=company_info_id,rejected=True).order_by('-id')

# Accept or reject update
class Accept_or_rejected_ApplyJob(UpdateAPIView):
    serializer_class = Accept_or_rejected_ApplyJobsSerializer
    queryset = ApplyJobs.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            user_id = instance.userInfo.userId
            job_name = instance.Post.Jobtitle.title_name 
            company_name = instance.comanyInfo.company_name 
            if user_id and instance.accepted:
                print('daxo')
                message = f'Congratulations, {user_id.first_name} {user_id.last_name}! Your application for the "{job_name}" position has been accepted in "{company_name}" company.'
                path = '/user/dashboard/'
                Notification.objects.create(user=user_id, message=message, path=path)
                send_accepted_users_email.delay(message,user_id.email)

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Date scheduled  
class ScheduleDate(UpdateAPIView):
    serializer_class = ScheduleDateSerializers
    queryset = ApplyJobs.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            scheduled_date = serializer.validated_data.get('schedule')
            max_users_per_date = 2
            scheduled_users_count = ApplyJobs.objects.filter(schedule=scheduled_date).count()
            if scheduled_users_count >= max_users_per_date:
                return Response(
                    {"detail": "Slot is full for this date. Please choose another date."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            
            user_id = instance.userInfo.userId
            job_name = instance.Post.Jobtitle.title_name 
            company_name = instance.comanyInfo.company_name 
            scheduled_date = instance.schedule
            if user_id and instance.accepted:
                message = f'Hi, {user_id.first_name} {user_id.last_name}! Your interview for the "{job_name}" position at "{company_name}" has been scheduled for {scheduled_date}.'
                path = '/user/dashboard/'
                Notification.objects.create(user=user_id, message=message, path=path)
                send_scheduled_users_email.delay(message,user_id.email)

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Company Notifications
class CompanyNotification(ListAPIView):
    serializer_class = CompanyNotificationSerializer
    pagination_class = None
    def get_queryset(self):
        company_id = self.kwargs['id']
        if company_id:
            return Notification.objects.filter(user_id=company_id).order_by('-timestamp')
        else:
            return Notification.objects.none()

# Company Home Page User LIsting
class CompanyHomeListing(ListAPIView):
    serializer_class = UserInfoListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['userId__first_name','userId__last_name','skills__skills']
    pagination_class = PageNumberPagination
    queryset = UserInfo.objects.all().exclude(userId__is_compleated=False).order_by('-created_at')

# Chating list
class UsersListing(ListAPIView):
    serializer_class = UsersChatListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['userInfo__userId__first_name','userInfo__userId__last_name','userInfo__userId__email']
    pagination_class = None

    def get_queryset(self):
        user_id = self.kwargs['id'] 
        return ApplyJobs.objects.filter(comanyInfo__userId=user_id, accepted=True).order_by('comanyInfo__userId', '-created_at').distinct('comanyInfo__userId')

class InviteUserCreate(CreateAPIView):
    serializer_class = UserInveiteSerializer
    queryset = InviteUsers.objects.all()


class InviteUserListUserside(ListAPIView):
    serializer_class = InviteUserListUsersides
    filter_backends = [SearchFilter]
    search_fields = ['comanyInfo__company_name','comanyInfo__industry','Post__job_category__field_name','Post__Jobtitle__title_name','Post__skills__skills']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_info_id = self.kwargs['id']
        return InviteUsers.objects.filter(userInfo=user_info_id)

# invite accepting
@api_view(['POST'])
def ivite_accepted_users(request, id):
    try:
        invite = get_object_or_404(InviteUsers, id=id)
        ApplyJobs.objects.create(
            comanyInfo=invite.comanyInfo,
            userInfo=invite.userInfo,
            Post=invite.Post
        )
        invite.delete()
        return Response({'message': 'Accepted successfully'}, status=status.HTTP_202_ACCEPTED)
    except:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

# invite rejecting
@api_view(['POST'])
def ivite_rejected_users(request, id):
    try:
        invite = get_object_or_404(InviteUsers, id=id)
        invite.delete()
        return Response({'message': 'Rejected successfully'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    

# User Side Jobs Post
class userListCompany(ListAPIView):
    serializer_class = UserlistCompanyserializer
    filter_backends = [SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['userId__first_name','userId__last_name','userId__email','skills__skills','jobField__field_name','jobTitle__title_name' ]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        comapny_info_id = self.kwargs['id']
        comapny_info = CompanyInfo.objects.get(id=comapny_info_id)
        context['comapny_info'] = comapny_info 
        return context
    
    def get_queryset(self):
        skills = self.request.GET.get('skills', '')
        job_category = self.request.GET.get('job_categories', '')
        job_title = self.request.GET.get('job_title', '') 

        # Convert query parameter strings to lists
        skills_list = skills.split(',') if skills else []
        job_category_list = job_category.split(',') if job_category else []
        job_title_list = job_title.split(',') if job_title else []
        queryset = UserInfo.objects.all()

        if skills_list:
            skills_query = Q()
            for skill in skills_list:
                skills_query |= Q(skills__skills__icontains=skill)
            queryset = queryset.filter(skills_query)

        if job_category_list:
            job_category_query = Q()
            for category in job_category_list:
                job_category_query |= Q(jobField__field_name__icontains=category)
            queryset = queryset.filter(job_category_query)

        if job_title_list:
            job_title_query = Q()
            for job_title in job_title_list:
                job_title_query |= Q(jobTitle__title_name__icontains=job_title)
            queryset = queryset.filter(job_title_query)
        if skills_list or job_category_list or job_title_list:
            queryset = queryset.exclude(userId__is_compleated=False,userId__is_active=False)
        queryset = queryset.distinct().order_by('-created_at')

        return queryset


# Unkow user Home Pge
class UnkownuserHome(ListAPIView):
    queryset = Post.objects.all().exclude(is_blocked=True,is_deleted=True)
    serializer_class = UnkownUserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['companyinfo__company_name','companyinfo__industry','companyinfo__company_type','companyinfo__streetaddress','companyinfo__state','companyinfo__country','companyinfo__city','skills__skills','job_category__field_name','Jobtitle__title_name' ,'description']
    
def seeimages(request):
    return render (request, 'company/email_template.html')