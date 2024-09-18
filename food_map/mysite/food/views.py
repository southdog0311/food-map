from hitcount.views import HitCountMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from .models import Place, Tag, TagManagement
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from hitcount.models import HitCount

def index(request):
    # 獲取所有餐廳
    places = Place.objects.all()
    places_with_hits = []
    
    for place in places:
        content_type = ContentType.objects.get_for_model(Place)
        hit_count, created = HitCount.objects.get_or_create(content_type=content_type, object_pk=place.id)
        places_with_hits.append({
            'place': place,
            'hit_count': hit_count.hits
        })
    
    # 總瀏覽人次（可選，根據需要計算）
    total_hit_count = sum(hit['hit_count'] for hit in places_with_hits)
    
    return render(request, 'food/index.html', {
        'places_with_hits': places_with_hits,
        'total_hit_count': total_hit_count
    })

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return render(request, 'food/place_detail.html', {'place': place})


# 搜尋功能
def search(request):
    query = request.GET.get('search')
    restaurant_name = request.GET.get('restaurant_name')
    cuisine_type = request.GET.get('cuisine_type')
    address = request.GET.get('address')
    tag_ids = request.GET.getlist('tags')

    search_results = Place.objects.all()

    # 篩選條件應用
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

# API：獲取所有餐廳的列表
def place_list(request):
    places = Place.objects.all()
    return JsonResponse({'places': list(places.values())})

# API：獲取單個餐廳的詳細資訊
def place_detail_api(request, place_id):
    place = Place.objects.filter(pk=place_id).values()
    if place.exists():
        return JsonResponse({'place': list(place)}, safe=False)
    else:
        return JsonResponse({'error': 'Place not found'}, status=404)

# 標籤列表視圖
class TagListView(ListView):
    model = Tag
    template_name = 'food/tag_list.html'
    context_object_name = 'tags'

# 標籤管理列表視圖
class TagManagementListView(ListView):
    model = TagManagement
    template_name = 'food/tag_management_list.html'
    context_object_name = 'tag_managements'
