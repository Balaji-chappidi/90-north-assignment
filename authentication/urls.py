from django.urls import path
from . import views

urlpatterns = [
    #Google OAuth
    path('google-authentication', views.GoogleAuthenticationView.as_view(), name='google-authentication'),
    path('google-callback', views.GoogleCallbackView.as_view(), name='google-callback'),

    #Google Drive
    path('google-drive-authentication', views.GoogleDriveAuthenticationView.as_view(), name='google-drive-authentication'),
    path('google-drive-callback', views.GoogleDriveCallbackView.as_view(), name='google-drive-callback'),
    path('google-drive-upload', views.GoogleDriveUploadView.as_view(), name='google-drive-upload'),
    path('google-drive-files-list', views.GoogleDriveListFilesView.as_view(), name='google-drive-files-list'),
    path('google-drive-download-file', views.GoogleDriveDownloadView.as_view(), name='google-drive-download-file'),
]