from rest_framework import  serializers

from .models import User 
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

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
    tokens=serializers.CharField(max_length=255,read_only=True)
    
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
