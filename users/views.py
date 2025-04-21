from django.shortcuts import render
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
       try:
           data = request.data
           serializer =  UserSerializer(data=data)
           if serializer.is_valid():
            serializer.save()
            return Response({
               "Message" : "User Created Successfully",
               "error" : False,
            }, status=status.HTTP_201_CREATED)
           else:
            return Response({
               "Message" : "An error occurred",
               "error" : True,
            },serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
