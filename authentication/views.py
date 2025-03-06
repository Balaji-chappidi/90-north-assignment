from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests

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
    
class GoogleDriveAuthenticationView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        context = {
            'success': 1,
            'message': 'Successfully generated Google authentication URL.',
            'data': {}
        }
        try:
            auth_url = (
                "https://accounts.google.com/o/oauth2/auth?"
                f"client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
                "response_type=code&scope=https://www.googleapis.com/auth/drive.file"
            )
            context["data"]["auth_url"] = auth_url
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
