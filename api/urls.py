from django.urls import path
from .views import *
from .view_profile import *
from rest_framework_simplejwt.views import TokenRefreshView
from .import views
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user-detail/<int:id>/',UserDetails.as_view(),name='user_details'),
    path('register/', UserRegister.as_view(),name="user_register"),
    path('googleregistration/', GoogleAuthendication.as_view(), name='googleregistration'),
    path('forgotpassword/', Forgotpassword.as_view(), name='Forgotpassword'),
    path('resetpassword/<uidb64>/', views.resetpassword, name='resetpassword'),
    path('restpassword/<int:id>/', UserRestpassword.as_view(), name='UserRestpassword'),

    path('UserInfoListCreateAPIView/', UserInfoListCreateAPIView.as_view(), name='UserInfoListCreateAPIView'),
    path('UserInfoDetails/<int:id>/', UserInfoDetails.as_view(), name='UserInfoDetails'),
    path('UserProfileUpdate/<int:id>/', UserProfileUpdate.as_view(), name='UserProfileUpdate'),
    path('Is_compleatedUpdate/<int:id>/', Is_compleatedUpdate.as_view(), name='Is_compleatedUpdate'),
    path('UpdateUseAccount/<int:id>/', UpdateUseAccount.as_view(), name='UpdateUseAccount'),
    
    path('ExperienceListCreateAPIView/', ExperienceListCreateAPIView.as_view(), name='ExperienceListCreateAPIView'),
    path('ExperienceDetails/<int:id>/', ExperienceDetails.as_view(), name='ExperienceDetails'),
    
    path('EducationListCreateAPIView/', EducationListCreateAPIView.as_view(), name='EducationListCreateAPIView'),
    path('EducationDetails/<int:id>/', EducationDetails.as_view(), name='EducationDetails'),
]