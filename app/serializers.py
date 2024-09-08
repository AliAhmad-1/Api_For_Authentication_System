from django.utils.encoding import smart_str
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework import serializers

from xml.dom import ValidationErr

from .utils import Util


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        extra_kwargs={
        'password':{'write_only':True}
        }


class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=100,required=True)
    
    class Meta:
        model=User
        fields=['username','password']


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(max_length=150,write_only=True,style={'input_type':'password'})
    password2=serializers.CharField(max_length=150,write_only=True,style={'input_type':'password'})

    class Meta:
        model=User
        fields=['password1','password2']

    def validate(self,data):
        # passwords validation
        password1, password2 = data.get('password1'), data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("password and confirm password  does't match")

        # user interactions
        user=self.context.get('user')
        user.set_password(password1)
        user.save()
        return data


class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    
    class Meta:
        model=User
        fields=['email']

    def validate(self,data):
        email=data.get('email')

        user = User.objects.filter(email=email)
        if user.exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://127.0.0.1:3000/reset-password/'+uid+'/'+token
            print(link)
            data={
                'subject':'Reset Your Password',
                'body':'Click Following Link to reset your password '+ link,
                'to_email':user.email
            }

            Util.send_email(data)

        else:
            raise ValidationErr('You are not a Registerd User')

        return data
        

class UserPasswordResetSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(max_length=150,write_only=True,style={'input_type':'password'})
    password2=serializers.CharField(max_length=150,write_only=True,style={'input_type':'password'})
    
    class Meta:
        model=User
        fields=['password1','password2']

    def validate(self,data):
        try:
            password1, password2 =data.get('password1'), data.get('password2')
            if password1 != password2:
                raise serializers.ValidationError("password and confirm password  does't match")
            
            uid=self.context.get('uid')
            token=self.context.get('token')
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or expired ')
            
            user.set_password(password1)
            user.save()
            return data
            
        except UnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or expired ')


class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    
    def validate(self,data):    
        self.token=data.get('refresh_token')
        return data
    
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
