from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from expenses.models import Expenses

from .permissions import IsOwner
from .serializers import ExpenseSerialier

from authentication.renderers import UserRenderer

class ExpenseList(ListCreateAPIView):
    serializer_class=ExpenseSerialier
    queryset=Expenses.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'
    renderer_classes=[UserRenderer]
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)  # send expenses owned by the current user
    

class ExpenseDetail(RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseSerialier
    queryset=Expenses.objects.all()
    permission_classes=[permissions.IsAuthenticated,IsOwner]
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    