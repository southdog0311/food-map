from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),
    path('search/', views.search, name='search'),
    #path('tags/', views.TagListView.as_view(), name='tag-list'),
    #path('tag-management/', views.TagManagementListView.as_view(), name='tag-management-list'),

]
