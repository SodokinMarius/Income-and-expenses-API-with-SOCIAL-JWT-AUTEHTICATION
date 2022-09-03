from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Income

from .permissions import IsOwner
from .serializers import IncomeSerialier


class IncomeList(ListCreateAPIView):
    serializer_class=IncomeSerialier
    queryset=Income.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)  # send expenses owned by the current user
    

class IncomeDetail(RetrieveUpdateDestroyAPIView):
    serializer_class=IncomeSerialier
    queryset=Income.objects.all()
    permission_classes=[permissions.IsAuthenticated,IsOwner]
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    