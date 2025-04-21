from django.shortcuts import render
from django.contrib.auth import authenticate
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

User = get_user_model()

# Create your views here.
class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "User Created Successfully",
                    "error": False,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": "An error occurred",
                    "error": True,
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            if username:
                user = User.objects.get(username=username)
         
            else:
                return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(username=user.username, password=password)
            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'error': False,
                    'message': 'Login successful',
                    'data': {
                        'email': user.email,  
                        'username' : user.username,
                        'accessToken': str(refresh.access_token),
                        'refreshToken': str(refresh),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': True, 'message': 'Incorrect login credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': True, 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)