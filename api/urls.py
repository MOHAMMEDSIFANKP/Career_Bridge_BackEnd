from django.urls import path
from .views import GoogleAuthendication,UserDetails,MyTokenObtainPairView,UserRegister
from rest_framework_simplejwt.views import TokenRefreshView
from .import views
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user-detail/<int:id>/',UserDetails.as_view(),name='user_details'),
    path('register/', UserRegister.as_view(),name="user_register"),
    path('googleregistration/', GoogleAuthendication.as_view(), name='googleregistration')
]