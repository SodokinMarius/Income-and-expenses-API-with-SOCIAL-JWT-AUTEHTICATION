from time import timezone
from django.db import models
from authentication.models  import User


class Expenses(models.Model):
    CATEGORIES_OPTIONS=[
        ('ONLINE_SERVICES','ONLINE_SERVICES'),
        ('TRAVEL','TRAVEL'),
        ('FOOD','FOOD'),
        ('FACTURE','FACTURE'),
        ('OTHERS','OTHERS')
    ]
    
    category=models.CharField(choices=CATEGORIES_OPTIONS,max_length=50)
    amount=models.DecimalField(max_digits=100,decimal_places=2)
    description=models.TextField(max_length=200)
    owner=models.ForeignKey(to=User,related_name='owner_expense',on_delete=models.CASCADE)
    creation_date=models.DateTimeField(auto_now_add=True)