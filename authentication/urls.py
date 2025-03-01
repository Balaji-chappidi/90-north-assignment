from django.urls import path
from . import views

urlpatterns = [
    path('google-authentication', views.GoogleAuthenticationView.as_view(), name='google-authentication'),
    path('google-callback', views.GoogleCallbackView.as_view(), name='google-callback'),
]