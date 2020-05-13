from django.urls import path
from .views  import *
# from django.views.decorators.cache import cache_page
from . import views
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('index/', HTMLView.as_view()),
    path('covidaapi/', CovidAPIView.as_view()),
    path('covid/', CovidView.as_view()),
    path('googlechart/', GoogleChartView.as_view()),
    path('create/', titanic_create, name='titanic'),
    path('titanic-list/',titaniclist, name="titaniclist"),
    path('edit-titanic/<pk>/',edittitanic, name="edittitanic"),
    url(r'api/users^$', views.UserCreate.as_view(), name='account-create'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # path('create/', TitanicViewForm.as_view()),
    # path('success/', TitanicViewForm.as_view()),
    # path('signup/', views.SignUp.as_view(), name='signup'),
]