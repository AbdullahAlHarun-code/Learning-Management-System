from django.shortcuts import render
# generic views
from rest_framework import generics
# permissions allowany
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# import register serializer
from .serializers import RegisterSerializer
# import user model 
from userauths.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer
import random
from rest_framework_simplejwt.tokens import RefreshToken
# status import
from rest_framework import status


class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

def generate_random_otp(length=7):
    return  ''.join([str(random.randint(0,9)) for i in range(length)])

class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            user.otp = generate_random_otp()
            
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.save()
            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"
            print('Link: ',link)
        return user

class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        otp = request.data.get('otp')   
        uuidb64 = request.data.get('uuidb64')
        password = request.data.get('password')

        user = User.objects.get(pk=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User does not exists'}, status=status.HTTP_400_NOT_FOUND)



