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
    
    path('seeimages/', views.seeimages, name='seeimages'),
]