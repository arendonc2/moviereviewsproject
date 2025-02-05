from django.shortcuts import render
from django.http import HttpResponse

#views

def home(request):
    return render(request, 'home.html', {'name':'Alejandro Rendon'})
def about(request):
    return render(request, 'about.html')