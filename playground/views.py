from django.shortcuts import render
from django.http import HttpResponse 
from store.models import Product

# Create your views here.
def say_hello(request):
    query_set = Product.objects.filter(last_update__year=2021)    
    return render(request, 'hello.html', {'name': 'Salisu Aminu Abdurrahman', 'products': list(query_set)})