from django.urls import path
from .views import *
from .import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('token/',AdminTokenObtainPairView.as_view(), name='AdminTokenObtainPairView'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
   path('get_chart_data/', views.get_chart_data, name='get_chart_data'),


   path('JobFieldListAndCreater/',JobFieldListAndCreater.as_view(), name="JobFieldList"),
   path('jobfieldlistandcreaterpagination/',JobFieldListAndCreaterPagination.as_view(), name="JobFieldListAndCreaterPagination"),
   path('jobfieldlistdeleted/',JobFieldListDeleted.as_view(), name="JobFieldListDeleted"),
   path('JobFieldDetails/<int:id>/',JobFieldDetails.as_view(), name="JobFieldDetails"),

   path('JobTitledListAndCreater/',JobTitledListAndCreater.as_view(), name="JobTitledListAndCreater"),
   path('jobtitledlistandpagiantions/',JobTitledListAndpagiantions.as_view(), name="JobTitledListAndpagiantions"),
   path('jobtitledblockedlist/',JobTitledBlockedList.as_view(), name="JobTitledBlockedList"),
   path('JobTitledDetails/<int:id>/',JobTitledDetails.as_view(), name="JobTitledDetails"),

    path('LanguageListCreateAPIView/',LanguageListCreateAPIView.as_view(), name="LanguageListCreateAPIView"),
    path('LanguagesdDetails/<int:id>/',LanguagesdDetails.as_view(), name="LanguagesdDetails"),
    
    path('SkillsListCreateAPIView/',SkillsListCreateAPIView.as_view(), name="SkillsListCreateAPIView"),
    path('skillslist/',SkillsList.as_view(), name="SkillsList"),
    path('blockedskillslist/',BlockedSkillsList.as_view(), name="BlockedSkillsList"),
    path('SkillsDetails/<int:id>/',SkillsDetails.as_view(), name="SkillsDetails"),
    
    path('userslist/',UsersList.as_view(), name="UsersList"),
    path('companyuserslist/',CompanyUsersList.as_view(), name="CompanyUsersList"),
    path('blockuserslist/',BlockUsersList.as_view(), name="BlockUsersList"),
    path('blockcompanyuserlist/',BlockCompanyUserList.as_view(), name="BlockCompanyUserList"),
    path('userblockunblock/<int:id>/',UserBlockUnblock.as_view(), name="UserBlockUnblock"),
    
    path('companylist/',CompanyList.as_view(), name="CompanyList"),
    path('CompanyVerifiedList/',CompanyVerifiedList.as_view(), name="CompanyVerifiedList"),
    path('companyblockedlist/',CompanyBlockedList.as_view(), name="CompanyBlockedList"),
    path('verifyandblock/<int:id>/',VerifyAndBlock.as_view(), name="VerifyAndBlock"),
    
    path('allpostlist/',ListAllPost.as_view(), name="ListAllPost"),
    path('listblockpost/',ListBlockPost.as_view(), name="ListBlockPost"),
    path('postblockedunblocked/<int:id>/',PostBlockedUnblocked.as_view(), name="PostBlockedUnblocked"),
    
    path('adminnotification/',AdminNotification.as_view(), name="AdminNotification"),
    path('adminnotificationread/<int:id>/',AdminNotificationRead.as_view(), name="AdminNotificationRead"),
    

]