from django.shortcuts import get_object_or_404, render
from .models import Place


def index(request):
    # return HttpResponse("Hello food!")
    places = Place.objects.all()
    return render(request, 'food/index.html', {'places': places})

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return render(request, 'food/place_detail.html', {'place': place})

'''def place_list(request):
    places = Place.objects.all()
    return render(request, 'place_list.html', {'places': places})'''