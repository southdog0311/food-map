from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from food.api import api  

urlpatterns = [
    path('', views.index, name='index'),
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),
    path('search/', views.search, name='search'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tag-management/', views.TagManagementListView.as_view(), name='tag-management-list'),
    path('food-admin/', admin.site.urls),
    path('api/places/', views.place_list, name='place_list'),
    path('api/places/<int:place_id>/', views.place_detail_api, name='place_detail_api'),
    path('api/', api.urls),  
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
