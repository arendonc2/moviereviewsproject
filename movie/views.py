from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

#views

def home(request):
    searchTerm = request.GET.get('searchMovie')
    name = "Alejandro Rendón"
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies, 'name': name})
def about(request):
    return render(request, 'about.html')