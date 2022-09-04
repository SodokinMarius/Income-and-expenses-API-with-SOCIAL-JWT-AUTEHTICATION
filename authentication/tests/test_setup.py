from rest_framework.test import  APITestCase
from faker import  Faker
from django.urls import reverse 

class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.faker=Faker()

        self.user_data={
            'email':self.faker.email(),
            'username':self.faker.email().split('@')[0],
            'password':self.faker.email().split('@')[0]
        }
        
        return super().setUp()

    def tearDown(self):
        return super().tearDown()