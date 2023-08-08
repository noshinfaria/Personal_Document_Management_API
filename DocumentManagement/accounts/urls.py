from django.urls import path
#now import the views.py file into this code
from . import views
from .views import SignUp, ListUsers, CustomAuthToken

urlpatterns=[
  path('userview/', ListUsers.as_view(), name="userview"),
  path('api-token-auth/', CustomAuthToken.as_view()),
  path('signup/', SignUp.as_view(), name="signup")
]