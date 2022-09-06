from .views import ExpensesSummaryStats, IncomeSummaryStats

from django.urls import path

urlpatterns = [
    path('user-expense-category',ExpensesSummaryStats.as_view(),name='user-expense-category'),
    path('user-income-source',IncomeSummaryStats.as_view(),name='user-income-source')

]
