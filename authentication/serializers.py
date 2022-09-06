import email
from string import ascii_letters
from rest_framework import  serializers

from .models import User 
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

#------- Import for password reset -----------

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from rest_framework import generics,status


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=8,write_only=True)

    class Meta:
        model=User 
        fields=['email','username','password']
    
    def validate(self,attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')

        if not username.isalnum():
            raise  serializers.ValidationError(
                "The username should contains only alphanumeric characters"
            )
            # return super().validate(attrs) #attrs represente les informations utilisateurs
        return attrs #attrs represente les informations utilisateurs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=255)
    
    class Meta:
        model=User
        fields=('token',)

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    password=serializers.CharField(max_length=255)
    username=serializers.CharField(max_length=255,read_only=True)
    #tokens=serializers.CharField(max_length=255,read_only=True)
    tokens=serializers.SerializerMethodField()
    
    
    #Fonction pour recuperer le token dans le variablee de serialization
    
    def get_tokens(self,obj):
        user=User.objects.get(email=obj['email'])
        
        return {
            "access":user.tokens['access'],
            "refresh":user.tokens['refresh']
        }
        
    
    class Meta:
        model=User 
        fields=['email','password','username','tokens']
        
    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        user=authenticate(email=email,password=password)
        
        if not user: 
            raise AuthenticationFailed("USer with these credentilas does not exists ! ")
        user.is_verified=True 
        if not user.is_active:
            raise AuthenticationFailed("This account is not active !!")
        if not user.is_verified:
            raise AuthenticationFailed("This account is not valid !!!")
       
        user_data={
            "email":user.email,
            "password":user.password,
            "tokens":user.create_tokens
        }
        return user_data
        return super().validate(attrs)


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh=serializers.CharField(max_length=250) 
    
    class Meta:
        fields=['refresh']


#------------ For password Reset -------------------------#
class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=8,max_length=50)
    
    class Meta:
        fields=['email']
    
    
    '''def validate(self, attrs):
        email=attrs.get('email','')
        return super().validate(attrs)
    '''
        
#---------------  For password setting -----------------#

class NewPasswordSettingSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=68,write_only=True)
    token=serializers.CharField(max_length=68,write_only=True)
    uidb64=serializers.CharField(max_length=68,write_only=True)
    
    class Meta:
        fields=['password','token','uidb64']
        
    def validate(self, attrs):
        password=attrs.get('password')
        token=attrs.get('token')
        uidb64=attrs.get('uidb64')
        
        user_id=force_str(urlsafe_base64_decode(uidb64))
        
        user=User.objects.get(id=user_id)
        
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise AuthenticationFailed('The reset link is invalid !!',status=status.HTTP_401_UNAUTHORIZED)
        
        #------------ Password Changing ------------ #
        user.set_password(password)
        user.save
        return user 
        return super().validate(attrs)


    
    
            
    