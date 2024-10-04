from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from .models import Place, Tag, TagManagement, HomePageView
from django.http import JsonResponse

# Index view to display all places and tags
def index(request):
    places = Place.objects.all()
    tags = Tag.objects.all()

    # Increment homepage view count if the user has not visited before
    if not request.session.get('has_visited_home', False):
        HomePageView.objects.create()  # Record a homepage visit
        request.session['has_visited_home'] = True  # Set session flag

    # Get the total homepage view count
    home_view_count = HomePageView.objects.count()

    return render(request, 'food/index.html', {
        'places': places,
        'tags': tags,
        'home_view_count': home_view_count,  # Pass view count to the template
    })

# Detail view for a specific place
def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place.view_count += 1  # Increment view count
    place.save()  # Save the updated view count to the database
    return render(request, 'food/place_detail.html', {
        'place': place,
        'view_count': place.view_count,
    })

# Search view to handle search queries and tag filtering
def search(request):
    query = request.GET.get('search', '')
    tag_ids = request.GET.getlist('tags')  # Get selected tags from the request
    search_results = Place.objects.all()

    # Filter by search query if provided
    if query:
        search_results = search_results.filter(name__icontains=query)

    # Filter by tags if selected
    if tag_ids:
        search_results = search_results.filter(tags__id__in=tag_ids).distinct()

    context = {
        'places': search_results,  # Pass filtered search results
        'tags': Tag.objects.all(),  # Pass all tags to allow filter refinement
        'query': query,  # Preserve the search query
    }
    return render(request, 'food/search_results.html', context)

# API endpoint to return a list of places in JSON format
def place_list(request):
    places = Place.objects.all()
    # Return place data as JSON
    return JsonResponse({'places': list(places.values())})

# API endpoint to return detailed information about a specific place in JSON format
def place_detail_api(request, place_id):
    place = Place.objects.filter(pk=place_id).values()
    if place.exists():
        # Return the place information as JSON
        return JsonResponse({'place': list(place)}, safe=False)
    else:
        # Return an error if the place is not found
        return JsonResponse({'error': 'Place not found'}, status=404)

# View to display a list of all tags
class TagListView(ListView):
    model = Tag
    template_name = 'food/tag_list.html'
    context_object_name = 'tags'

# View to manage tags for each place
class TagManagementListView(ListView):
    model = TagManagement
    template_name = 'food/tag_management_list.html'
    context_object_name = 'tag_managements'
