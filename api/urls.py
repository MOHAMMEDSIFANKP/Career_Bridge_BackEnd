from django.urls import path
from .views import *
from .view_profile import *
from rest_framework_simplejwt.views import TokenRefreshView
from .import views
from .import view_profile
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user-detail/<int:id>/',UserDetails.as_view(),name='user_details'),
    path('register/', UserRegister.as_view(),name="user_register"),
    path('Resend_registration_link/', views.Resend_registration_link,name="Resend_registration_link"),
    path('googleregistration/', GoogleAuthendication.as_view(), name='googleregistration'),
    path('forgotpassword/', Forgotpassword.as_view(), name='Forgotpassword'),
    path('resetpassword/<uidb64>/', views.resetpassword, name='resetpassword'),
    path('restpassword/<int:id>/', UserRestpassword.as_view(), name='UserRestpassword'),
# Reset password in profile
    path('reset_password/<int:id>/', view_profile.reset_password, name='reset_password'),

    path('UserInfoListCreateAPIView/', UserInfoListCreateAPIView.as_view(), name='UserInfoListCreateAPIView'),
    path('UserInfoDetails/<int:id>/', UserInfoDetails.as_view(), name='UserInfoDetails'),
    path('UserProfileUpdate/<int:id>/', UserProfileUpdate.as_view(), name='UserProfileUpdate'),
    path('Is_compleatedUpdate/<int:id>/', Is_compleatedUpdate.as_view(), name='Is_compleatedUpdate'),
    path('updateuseaccount/<int:id>/', UpdateUseAccount.as_view(), name='UpdateUseAccount'),
    path('remove_skill/', view_profile.remove_skill, name='remove_skill'),
    
    path('ExperienceListCreateAPIView/', ExperienceListCreateAPIView.as_view(), name='ExperienceListCreateAPIView'),
    path('ExperienceDetails/<int:id>/', ExperienceDetails.as_view(), name='ExperienceDetails'),
    
    path('EducationListCreateAPIView/', EducationListCreateAPIView.as_view(), name='EducationListCreateAPIView'),
    path('EducationDetails/<int:id>/', EducationDetails.as_view(), name='EducationDetails'),
    
    path('userrelatedjobs/<int:id>/', UserRelatedJobs.as_view(), name='UserRelatedJobs'),
    path('userpostlist/<int:id>/', UserPost.as_view(), name='UserPost'),
    
    path('UserApplyPostList/<int:id>/', UserApplyPostList.as_view(), name='UserApplyPostList'),
    path('UserAcceptedApplyPostList/<int:id>/', UserAcceptedApplyPostList.as_view(), name='UserAcceptedApplyPostList'),
    path('UserPendingApplyPostList/<int:id>/', UserPendingApplyPostList.as_view(), name='UserPendingApplyPostList'),
    
    path('notificationconut/<int:id>/', views.Notification_count, name='Notification_count'),
    path('usernotification/<int:id>/', userNotification.as_view(), name='userNotification'),
    path('NotificationRead/<int:id>/', NotificationRead.as_view(), name='NotificationRead'),

    path('CompaniesList/<int:id>/',CompaniesList.as_view(),name='CompaniesList'),
   

    
]