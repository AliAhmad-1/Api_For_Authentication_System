from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegitserView(APIView):
    def post(self,request,format=None):
        serializers=UserRegisterSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user=serializers.save()
            token=get_tokens_for_user(user)
            return Response({'msg':'your account created successfully','token':token},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request,format=None):
        serializers=UserLoginSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            username=serializers.data.get('username')
            password=serializers.data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'msg':'Login Success','access_token':token['access'],'refresh_token':token['refresh']},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'non_field_errors':['Email or Password not Valid ']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializers=UserProfileSerializer(request.user)
        return Response(serializers.data,status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializers=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save
            return Response({'msg':'password was updated successfully '},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):

    def post(self,request,format=None):
        serializers=SendPasswordResetEmailSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save
            return Response({'msg':'password reset link send , Please check your email '},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
        serializers=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializers.is_valid(raise_exception=True):
            serializers.save
            return Response({'msg':'password reset successfully'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializers=LogoutSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response({'msg':'User logout succussfully'},status=status.HTTP_204_NO_CONTENT)
