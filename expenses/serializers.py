
from rest_framework import serializers
from .models import Expenses
class ExpenseSerialier(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields='__all__'
        read_only_fields=('id','owner','creation_date',)