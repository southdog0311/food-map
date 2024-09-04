from django.shortcuts import get_object_or_404, render
from .models import Place, Tag, TagManagement
from django.views.generic import ListView

def index(request):
    places = Place.objects.all()
    tags = Tag.objects.all()  # 傳遞標籤列表給模板
    return render(request, 'food/index.html', {'places': places, 'tags': tags})

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return render(request, 'food/place_detail.html', {'place': place})

def search(request):
    query = request.GET.get('search')
    restaurant_name = request.GET.get('restaurant_name')
    cuisine_type = request.GET.get('cuisine_type')
    address = request.GET.get('address')
    tag_ids = request.GET.getlist('tags')

    search_results = Place.objects.all()

    # 每個篩選條件獨立應用，允許條件為空
    if query:
        search_results = search_results.filter(name__icontains=query)

    if restaurant_name:
        search_results = search_results.filter(name__icontains=restaurant_name)

    if cuisine_type:
        search_results = search_results.filter(cuisine_type__icontains=cuisine_type)

    if address:
        search_results = search_results.filter(address__icontains=address)

    if tag_ids:
        search_results = search_results.filter(tags__id__in=tag_ids).distinct()

    context = {
        'places': search_results,
        'tags': Tag.objects.all(),  # 傳遞標籤列表給模板
    }
    return render(request, 'food/search_results.html', context)

class TagListView(ListView):
    model = Tag
    template_name = 'food/tag_list.html'
    context_object_name = 'tags'

class TagManagementListView(ListView):
    model = TagManagement
    template_name = 'food/tag_management_list.html'
    context_object_name = 'tag_managements'
