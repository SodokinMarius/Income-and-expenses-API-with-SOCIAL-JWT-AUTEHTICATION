import  datetime
from rest_framework.views import APIView
from rest_framework import  status
from expenses.models import Expenses
from income.models import Income
from rest_framework.response import Response

class ExpensesSummaryStats(APIView):    
    
    # --------- Fonction retournant le montant total de chaque categorie
    def get_amount_for_category(self,expenses,category):
        total_amount=0
        expenses_usable=expenses.filter(category=category)
        for expense in expenses_usable:
            total_amount+=expense.amount
            
        return {"total_amount":str(total_amount)}
            
    #------ Fonction qui retourne la categorie -------
    def get_category(self,expense):
        return expense.category
    
    def get(self,request):
        todays_date=datetime.datetime.today()            #<------ Recuperer la date d'aujourd'hui
        one_year_ago=todays_date-datetime.timedelta(days=30*12)  # A partir de la date actuelle, compter un an
        
        #filter les depenses fait depuis 1 an et qui appartienne au user
        expenses=Expenses.objects.filter(owner=request.user,creation_date__gte=one_year_ago,creation_date__lte=todays_date)
        
        summary={}
        categories=list(set(map(self.get_category,expenses))) 
         
        #Calculer et regrouper les dpenses par categorie
        for expense in expenses:
            
            for category in categories:
                summary[category]=self.get_amount_for_category(expenses,category)
        return Response({"category_data":summary},status=status.HTTP_200_OK)


class IncomeSummaryStats(APIView):    
    
    # --------- Fonction retournant le montant total de chaque categorie
    def get_amount_for_source(self,incomes,source):
        total_amount=0
        incomes_usable=incomes.filter(source=source)
        for income in incomes_usable:
            total_amount+=income.amount
            
        return {"total_amount":str(total_amount)}
            
    #------ Fonction qui retourne la categorie -------
    def get_source(self,income):
        return income.source
    
    def get(self,request):
        todays_date=datetime.datetime.today()            #<------ Recuperer la date d'aujourd'hui
        one_year_ago=todays_date-datetime.timedelta(days=30*12)  # A partir de la date actuelle, compter un an
        
        #filter les depenses fait depuis 1 an et qui appartienne au user
        incomes=Income.objects.filter(owner=request.user,creation_date__gte=one_year_ago,creation_date__lte=todays_date)
        
        summary={}
        sources=list(set(map(self.get_source,incomes))) 
         
        #Calculer et regrouper les dpenses par categorie
        for income in incomes:
            
            for source in sources:
                summary[source]=self.get_amount_for_source(incomes,source)
        return Response({"income_data":summary},status=status.HTTP_200_OK)