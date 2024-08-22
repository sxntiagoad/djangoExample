from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64
# Create your views here.
def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        # Filtra las películas que contienen el término de búsqueda en el título o descripción
        movies = Movie.objects.filter(title__icontains=searchTerm) | Movie.objects.filter(description__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    
    return render(request, 'home.html', {'name': 'Santiago Alvarez','searchTerm': searchTerm, 'movies': movies})
def about(request):
    return render(request,'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')  # Usar 'Agg' backend para evitar problemas con entornos sin display

    all_movies = Movie.objects.all()

    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    for movie in all_movies:
        # Contar películas por año
        year = str(movie.year) if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

        # Contar películas por género, considerando solo el primer género
        genre = movie.genre.split(',')[0] if movie.genre else "None"
        movie_counts_by_genre[genre] = movie_counts_by_genre.get(genre, 0) + 1

    # Gráfica de películas por año
    buffer_year = io.BytesIO()
    plt.bar(movie_counts_by_year.keys(), movie_counts_by_year.values(), width=0.5)
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()

    # Convertir la gráfica de películas por año a base64
    image_png_year = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_png_year).decode('utf-8')

    # Gráfica de películas por género
    buffer_genre = io.BytesIO()
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), width=0.5)
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    # Convertir la gráfica de películas por género a base64
    image_png_genre = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')

    # Renderizar la plantilla con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })