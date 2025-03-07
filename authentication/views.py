from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests
import json

class GoogleAuthenticationView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        context = {
            'success': 1,
            'message': 'Successfully generated Google authentication URL.',
            'data': {}
        }
        try:
            google_auth_url = (
                "https://accounts.google.com/o/oauth2/auth?"
                f"client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
                "response_type=code&scope=openid%20email%20profile"
            ) 
            context['data']['auth_url'] = google_auth_url
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

class GoogleCallbackView(APIView):

    def get(self, request):
        context = {
            'success': 1,
            'message': 'Successfully retrieved the user data.',
            'data': {}
        }
        try:
            code = request.GET.get('code')
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
                "code": code,
            }
            token_response = requests.post(token_url, data=token_data).json()
            access_token = token_response.get("access_token")

            user_info = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
            context['data'] = user_info
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
# class GoogleDriveAuthenticationView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request):
#         context = {
#             'success': 1,
#             'message': 'Successfully generated Google authentication URL.',
#             'data': {}
#         }
#         try:
#             auth_url = (
#                 "https://accounts.google.com/o/oauth2/auth?"
#                 f"client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
#                 "response_type=code&scope=https://www.googleapis.com/auth/drive.file"
#             )
#             context["data"]["auth_url"] = auth_url
#         except Exception as e:
#             context['success'] = 0
#             context['message'] = str(e)
#         return Response(context)

class GoogleDriveAuthenticationView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        context = {
            'success': 1,
            'message': 'Successfully generated Google Drive authentication URL.',
            'data': {}
        }
        try:
            auth_url = (
                "https://accounts.google.com/o/oauth2/auth?"
                f"client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_DRIVE_REDIRECT_URI}&"
                "response_type=code&scope=https://www.googleapis.com/auth/drive.file&access_type=offline"
            )
            context['data']['auth_url'] = auth_url
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
class GoogleDriveCallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        context = {
            'success': 1,
            'message': 'Successfully authenticated with Google Drive.',
            'data': {}
        }
        try:
            code = request.GET.get('code')
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_DRIVE_REDIRECT_URI,
                "grant_type": "authorization_code",
                "code": code,
            }
            token_response = requests.post(token_url, data=token_data).json()
            context['data'] = {
                "access_token": token_response.get("access_token"),
                "refresh_token": token_response.get("refresh_token"),
                "expires_in": token_response.get("expires_in")
            }
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

class GoogleDriveUploadView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {
            'success': 1,
            'message': 'File uploaded successfully to Google Drive.',
            'data': {}
        }
        try:
            access_token = request.data.get("access_token")
            file = request.FILES.get("file")
            headers = {"Authorization": f"Bearer {access_token}"}
            metadata = {
                "name": file.name,
                "mimeType": file.content_type
            }

            files = {
                'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                'file': (file.name, file, file.content_type)
            }
            response = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", 
                                     headers=headers, 
                                     files=files).json()
            context['data'] = response
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

class GoogleDriveListFilesView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        context = {
            'success': 1,
            'message': 'Successfully retrieved Google Drive files.',
            'data': {}
        }
        try:
            access_token = request.GET.get("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers).json()
            context['data'] = response
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)

class GoogleDriveDownloadView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, file_id):
        context = {
            'success': 1,
            'message': 'Successfully retrieved file from Google Drive.',
            'data': {}
        }
        try:
            access_token = request.GET.get("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media", headers=headers)

            context['data']['file_content'] = response.content.decode("utf-8")
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)


