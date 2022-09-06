
from rest_framework import generics,status,views

from .serializers import  (
    RegisterSerializer,
    PasswordResetSerializer,
    NewPasswordSettingSerializer
    )
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
from .serializers import EmailVerificationSerializer,LoginSerializer

#swagger import
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#import for token obtain views
from rest_framework_simplejwt.views import  TokenRefreshView

#import the renderer
from .renderers import UserRenderer


#import for token refresh view 
from rest_framework_simplejwt.views import TokenRefreshView


#------- Import for password reset -----------

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse 

from rest_framework.response import Response 
from .utils import Util 
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer
    
    renderer_classes=(UserRenderer,)

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
        'token',in_=openapi.IN_QUERY,description='Email verifification view',type=openapi.TYPE_STRING
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

            

class LoginAPIView(generics.GenericAPIView):
     serializer_class=LoginSerializer
     
     def post(self,request):
         serializer=self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         response ={
             "message":"User connected successfully !!",
             "data":serializer.data
         }
         return Response(data=response,status=status.HTTP_200_OK)



'''class TokenRefreshView(TokenRefreshView):
    serializer_class=super().serializer_class
    
    def post(self,request):
        token=request.data 
     
        try:
            playload=jwt.decode(token,settings.SECRET_KET,algorithms=['HS256']) 
            user=User.objects.get(id=playload['user_id'])
            
            current_site=get_current_site(request).domain
            access=super().get_tok
        except:
            pass 
            #    ------ la suite .... ------#'''

# --------------- Classes for password resset ---------------------- #

class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class=PasswordResetSerializer
    
    def post(self,request):
        serializer=self.serializer_class(data=request.data)        
        email=request.data['email']
        
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)           
            encode=urlsafe_base64_encode(smart_bytes(user.id))   #<---- Pour coder l'ID de User
            token=PasswordResetTokenGenerator().make_token(user)   # Pour generer un token  qui correspond à User uniquement
            
            current_site=get_current_site(request=request).domain  #<------ La donnée saisie et recupérée est renvoyé en paramètre | respect du format envoyé par la vue

            relativeLink=reverse('passord-reset-confirm',kwargs={'uidb64':encode,'token':token})  #<---- Passage des paramètre au Reverse 

            absurl='http://'+current_site+relativeLink
            email_body='Hello \n Use link below reset your password \n'+absurl    
            data={'email_body':email_body,'email_to':user.email,'email_subject':'reset your password'}

            Util.send_email(data)        
        message="We have sent you a link to reset your password ! \n Then, consult your Email"
        return Response({"success":message},status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class=NewPasswordSettingSerializer
    
    def get(self,request,uidb64,token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64)) #<------ Decodage de l'ID
            user=User.objects.get(id=user_id)       #<------------ Recuperation du User dont l'Id est decodé
            
            if not PasswordResetTokenGenerator().check_token(user,token):   #Decodage du token du User recupéré
                return Response({'error':'This token is not valid ! PLease, request a new one'})
            
            return Response({'succes':True,'message': 'Credentials valid !!', 'uidb64':uidb64,'token':token})
                   
        except DjangoUnicodeDecodeError as identifier:
               if not PasswordResetTokenGenerator().check_token(user,token):
                   return Response({'error':'Token is not valid, please request a new one !!'})

class NewPasswordSettingViewAPI(generics.GenericAPIView):
    serializer_class=NewPasswordSettingSerializer
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":True,"message":"Password reset success"},status=status.HTTP_200_OK)
        
        
     
     