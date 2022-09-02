from django.shortcuts import render

from rest_framework import generics,status,views

from .serializers import  RegisterSerializer
from rest_framework.response import Response 
from django.urls import reverse

from .models import User

from .utils import Util

from rest_framework_simplejwt.tokens import RefreshToken

#Importation des packages du site courant
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse 

import  jwt #<---- for decoding
from django.conf import settings 

#Import serializer class
from .serializers import EmailVerificationSerializer

#swagger import
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer

    def post(self,request):
        user=request.data 
        serializer=self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)

        serializer.save()
 
        user_data=serializer.data 

        #Recupération de l'utilisateur créer
        user=User.objects.get(email=user_data['email'])

        current_site=get_current_site(request).domain


        relativeLink=reverse('verify_email')

        token=RefreshToken.for_user(user).access_token #Obtention des Tokens  (d'accès) pour l'utilisateur
         
        absurl='http://'+current_site+relativeLink+"?token="+str(token)

        email_body='Hi ! '+user.username+' Use link below to verify email \n'+absurl
 
        data={'email_body':email_body,'email_to':user.email,'email_subject':'verify your email'}

        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class=EmailVerificationSerializer
    
    token_parameter_config=openapi.Parameter(
        'token',in_=openapi.IN_QUERY,description='Email  verifification view',type=openapi.TYPE_STRING
        )   
     
    @swagger_auto_schema(manual_parameters=[token_parameter_config])   
    def get(self,request):
        token=request.GET.get('token')

        try:
            playload=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])

            print(f"test viewing username =========== {playload['user_id']}")
            user=User.objects.get(id=playload['user_id'])
            user.is_verified=True 
            user.save()
            return Response({'email':'succesfuly activated !'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired !'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return  Response({'error':'Invalid token !'},status=status.HTTP_400_BAD_REQUEST)

            

         