from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
# Create your views here.
def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        # Filtra las películas que contienen el término de búsqueda en el título o descripción
        movies = Movie.objects.filter(title__icontains=searchTerm) | Movie.objects.filter(description__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})
def about(request):
    return render(request,'about.html')