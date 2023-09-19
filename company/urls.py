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
]