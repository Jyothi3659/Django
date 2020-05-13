from django.urls import path
from .views  import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('activity/paginate/', GroupsView.as_view()),
    path('activity/filter/', ActivityFilterAPIView.as_view()),
    path('activity/', ActivityAPIView.as_view()),
    path('milestone/', MileStoneAPIView.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]