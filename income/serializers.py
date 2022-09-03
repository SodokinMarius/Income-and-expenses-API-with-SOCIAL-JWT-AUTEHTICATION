
from rest_framework import serializers
from .models import Income
class IncomeSerialier(serializers.ModelSerializer):
    class Meta:
        model=Income
        fields='__all__'
        read_only_fields=('id','owner','creation_date',)