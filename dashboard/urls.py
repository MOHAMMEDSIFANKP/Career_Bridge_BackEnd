from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('token/',AdminTokenObtainPairView.as_view(), name='AdminTokenObtainPairView'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('JobFieldListAndCreater/',JobFieldListAndCreater.as_view(), name="JobFieldList"),
   path('JobFieldDetails/<int:id>/',JobFieldDetails.as_view(), name="JobFieldDetails"),

   path('JobTitledListAndCreater/',JobTitledListAndCreater.as_view(), name="JobTitledListAndCreater"),
   path('JobTitledDetails/<int:id>/',JobTitledDetails.as_view(), name="JobTitledDetails"),

    path('LanguageListCreateAPIView/',LanguageListCreateAPIView.as_view(), name="LanguageListCreateAPIView"),
    path('LanguagesdDetails/<int:id>/',LanguagesdDetails.as_view(), name="LanguagesdDetails"),
    
    path('SkillsListCreateAPIView/',SkillsListCreateAPIView.as_view(), name="SkillsListCreateAPIView"),
    path('SkillsDetails/<int:id>/',SkillsDetails.as_view(), name="SkillsDetails"),
    
    path('userslist/',UsersList.as_view(), name="UsersList"),
    path('userblockunblock/<int:id>/',UserBlockUnblock.as_view(), name="UserBlockUnblock"),
    
    path('companylist/',CompanyList.as_view(), name="CompanyList"),
    path('verifyandblock/<int:id>/',VerifyAndBlock.as_view(), name="VerifyAndBlock"),
    
    path('adminnotification/',AdminNotification.as_view(), name="AdminNotification"),
    path('adminnotificationread/<int:id>/',AdminNotificationRead.as_view(), name="AdminNotificationRead"),


]