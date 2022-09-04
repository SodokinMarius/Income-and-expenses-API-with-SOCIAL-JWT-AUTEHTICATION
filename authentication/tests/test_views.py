from inspect import stack
from urllib import response
from .test_setup import TestSetUp
from rest_framework import generics,status,views
from authentication.models import User 


class TestViews(TestSetUp):
    
    def test_user_register(self):
        register=self.client.post(self.register_url, self.user_data,format="json")
        self.assertEqual(register.status_code,status.HTTP_201_CREATED)
        self.assertEqual(register.data['email'],self.user_data['email'])
        self.assertEqual(register.data['username'],self.user_data['username'])
        self.assertEqual(User.objects.count(),1)

    def test_register_with_without_data(self):
        count=User.objects.count()
        response=self.client.post(self.register_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),count)
    
    def  test_login_user_with_invalid_data(self):
        register=self.client.post(self.register_url, self.user_data,format="json")
        self.assertEqual(register.status_code,status.HTTP_201_CREATED)

        response=self.client.post(self.login_url,self.user_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_user_after_verification(self):
        response=self.client.post(self.register_url,self.user_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        user_mail=self.user_data['email']
        user=User.objects.get(email=user_mail)
        
        self.assertEqual(user.email,self.user_data['email'])
        user.is_verified=True
        log=self.client.post(self.login_url,self.user_data,format='json')
        self.assertEqual(log.status_code,status.HTTP_200_OK)
        

        