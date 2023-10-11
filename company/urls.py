from django.urls import path
from .views import *
from .import views
urlpatterns = [

    path('company-detail/<int:id>/',CompanyUserDetails.as_view(),name='user_details'),
    path('register/', CompanyRegister.as_view(),name="user_register"),
    path('googleregistration/', CompanyGoogleAuthendication.as_view(), name='googleregistration'),
    
    path('companyinfolistcreateapview/', CompanyInfoListCreateAPIView.as_view(), name='CompanyInfoListCreateAPIView'),
    path('companydetails/<int:id>/', CompanyDetails.as_view(), name='CompanyDetails'),
    
    path('companyPostlistCreateapiview/', CompanyPostListCreateAPIView.as_view(), name='CompanyPostListCreateAPIView'),
    path('listofcompanypost/<int:id>/', Listofcompanypost.as_view(), name='Listofcompanypost'),
    path('listofcompanypostarchived/<int:id>/', ListofcompanypostArchived.as_view(), name='ListofcompanypostArchived'),
    path('listofcompanypostblocked/<int:id>/', ListofcompanypostBlocked.as_view(), name='ListofcompanypostBlocked'),
    path('companypostdetails/<int:id>/', CompanyPostDetails.as_view(), name='CompanyPostDetails'),
    path('companypostupdate/<int:id>/', CompanyPostUpdate.as_view(), name='CompanyPostUpdate'),
    path('companypostbolckUnblock/<int:id>/', CompanyPostBolckUnblock.as_view(), name='CompanyPostBolckUnblock'),
    
    path('applyjobscreation/', ApplyJobsCreation.as_view(), name='ApplyJobsCreation'),
    path('companyapplypostList/<int:id>/', CompanyApplyPostList.as_view(), name='CompanyApplyPostList'),
    path('pendingapplyJob/<int:id>/', Pending_ApplyJob.as_view(), name='Pending_ApplyJob'),
    path('acceptedapplyJob/<int:id>/', Accepted_ApplyJob.as_view(), name='Accepted_ApplyJob'),
    path('rejectedapplyJob/<int:id>/', Rejected_ApplyJob.as_view(), name='Rejected_ApplyJob'),
    path('Accept_or_rejected_ApplyJob/<int:id>/', Accept_or_rejected_ApplyJob.as_view(), name='Accept_or_rejected_ApplyJob'),
    path('scheduledate/<int:id>/', ScheduleDate.as_view(), name='ScheduleDate'),
    
    path('CompanyNotification/<int:id>/', CompanyNotification.as_view(), name='CompanyNotification'),
    path('CompanyHomeListing/', CompanyHomeListing.as_view(), name='CompanyHomeListing'),
    
    path('userslisting/<int:id>/', UsersListing.as_view(), name='UsersListing'),
    
    path('inviteusercreate/', InviteUserCreate.as_view(), name='InviteUserCreate'),
    path('inviteUserlistuserside/<int:id>/', InviteUserListUserside.as_view(), name='InviteUserListUserside'),
    path('iviteacceptedusers/<int:id>/', views.ivite_accepted_users, name='ivite_accepted_users'),
    path('iviterejectedusers/<int:id>/', views.ivite_rejected_users, name='ivite_rejected_users'),
    
    path('userListCompany/<int:id>/', userListCompany.as_view(), name='userListCompany'),
    
    path('UnkownuserHome/',UnkownuserHome.as_view(),name='UnkownuserHome'),

    path('seeimages/', views.seeimages, name='seeimages'),
]