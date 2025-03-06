from django.urls import path
from . import views

urlpatterns = [
    #Google OAuth
    path('google-authentication', views.GoogleAuthenticationView.as_view(), name='google-authentication'),
    path('google-callback', views.GoogleCallbackView.as_view(), name='google-callback'),

    #Google Drive
    path('google-drive-authentication', views.GoogleDriveAuthenticationView.as_view(), name='google-drive-authentication'),
]