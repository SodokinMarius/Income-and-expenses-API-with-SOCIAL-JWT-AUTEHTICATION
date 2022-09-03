from time import timezone
from django.db import models
from authentication.models  import User


class Income(models.Model):
    SOURCE_OPTIONS=[
        ('SALARY','SALARY'),
        ('BUSINESSES','BUSINESSES'),
        ('FIVEN','GIVEN'),
        ('FARMS','FARMS'),
        ('OTHERS','OTHERS')
    ]
    
    source=models.CharField(choices=SOURCE_OPTIONS,max_length=50)
    amount=models.DecimalField(max_digits=100,decimal_places=2)
    description=models.TextField(max_length=200)
    owner=models.ForeignKey(to=User,related_name='owner_income',on_delete=models.CASCADE)
    creation_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
            ordering=['-creation_date']
    
    def __str__(self):
        return '{} | {} | {}'.format(self.source,self.amount,self.owner)