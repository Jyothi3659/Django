# from django.urls import path
# from .views  import *
# from django.conf.urls import url
# urlpatterns = [
#     path('register/', UserCreateAPIView.as_view()),
#     path('login/', UserLoginAPIView.as_view()),
#     path('logout/', UserLogoutview.as_view())   
# ]

from rest_framework import routers

from .views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
