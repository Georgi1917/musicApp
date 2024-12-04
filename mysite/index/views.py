from django.shortcuts import render
from album_creation.models import Playlist

# Create your views here.

def home_page_index(request):
    
    return render(request, "index/index.html")
    
def show_main_page(request):
    
    return render(request, "index/main-page.html")