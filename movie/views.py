from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64

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

def singup(request):
    email = request.GET.get('email')
    return render(request, 'singup.html', {'email':email})

def statistics_view(request): 
    matplotlib.use('Agg') 
    
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') # Obtener todos los años de las películas 

    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('year') #Obtener generos de las peliculas

    movie_counts_by_year = {} # Crear un diccionario para almacenar la cantidad de películas por año

    movie_counts_by_genre = {}

    for year in years: # Contar la cantidad de películas por año 
        if year: 
            movies_in_year = Movie.objects.filter(year=year) 
        else: 
            movies_in_year = Movie.objects.filter(year__isnull=True) 
            year = "None" 
        count   = movies_in_year.count() 
        movie_counts_by_year[year] = count

    for genre in genres: # contar cantidad de peliculas por genero
        if genre:
            movies_in_genre = Movie.objects.filter(genre=genre)
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
        count = movies_in_genre.count()
        movie_counts_by_genre[genre] = count

    # Configuración de la gráfica de películas por año
    plt.figure(figsize=(12, 6))  # Tamaño de la figura
    
    # Gráfica de películas por año
    plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, primera gráfica
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    # Gráfica de películas por género
    plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, segunda gráfica
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})