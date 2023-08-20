from django.urls import path
from .views import CompanyGoogleAuthendication,CompanyUserDetails,CompanyRegister
from .import views
urlpatterns = [

    path('company-detail/<int:id>/',CompanyUserDetails.as_view(),name='user_details'),
    path('register/', CompanyRegister.as_view(),name="user_register"),
    path('googleregistration/', CompanyGoogleAuthendication.as_view(), name='googleregistration')
]