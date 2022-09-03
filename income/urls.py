from django.urls import path

from .views import IncomeList,IncomeDetail


urlpatterns = [
    path('incomes/',IncomeList.as_view(),name='incomes'),
    path('incomes/<int:pk>/',IncomeDetail.as_view(),name='income-detail')
]