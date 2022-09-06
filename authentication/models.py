from django.db import models

from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager,PermissionsMixin)

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError('User should have a username !')
        if email is None:
            raise TypeError('Users should have an Email!')
        
        user=self.model(username=username,email=self.normalize_email(email))

        user.set_password(password)
        user.save()
        return user
    
    #Methode de création du superuser
    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError('Password should not be none!')
        #if email is None:
           # raise TypeError('Users should have an Email !')
        
        user=self.create_user(username,email,password)

        user.is_superuser=True 
        user.is_staff=True 
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=255,unique=True,db_index=True)
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    tokens=models.CharField(max_length=68)
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
 
    objects=UserManager()  # Telling to Django how to manage objects

    def __str__(self):
        return self.email
    
    def create_tokens(self): # Important de definir d'abord le las setting AUTH_USER_MODEL
        token=RefreshToken.for_user(self)
        
        return {
            "refresh":str(token),
            "access":str(token.access_token)
        }






    


