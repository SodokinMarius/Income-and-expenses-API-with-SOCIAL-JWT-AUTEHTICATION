from django.urls import path

from .views import ExpenseList,ExpenseDetail


urlpatterns = [
    path('expenses/',ExpenseList.as_view(),name='expenses'),
    path('expenses/<int:pk>/',ExpenseDetail.as_view(),name='expense-detail')
]