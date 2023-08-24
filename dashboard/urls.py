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
]