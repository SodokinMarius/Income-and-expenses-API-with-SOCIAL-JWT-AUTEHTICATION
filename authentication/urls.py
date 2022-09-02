from django.urls import path,include 

from .views import RegisterView,VerifyEmail


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('verify_email/',VerifyEmail.as_view(),name='verify_email'),

]
