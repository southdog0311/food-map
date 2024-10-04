from django.urls import path, include
from . import views
from food.api import api as food_api  # 假設在 food.api 中定義了你的 NinjaAPI 物件

urlpatterns = [
    # 主頁：顯示所有餐廳
    path('', views.index, name='index'),

    # 餐廳詳細頁面：顯示指定餐廳的詳細資訊
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),

    # 搜尋功能：依據關鍵字和標籤搜尋餐廳
    path('search/', views.search, name='search'),

    # 標籤列表：顯示所有標籤
    path('tags/', views.TagListView.as_view(), name='tag-list'),

    # 標籤管理列表：顯示標籤管理的紀錄
    path('tag-management/', views.TagManagementListView.as_view(), name='tag-management-list'),

    # REST API：獲取所有餐廳的列表 (返回 JSON)
    path('api/places/', views.place_list, name='place_list'),

    # REST API：獲取特定餐廳的詳細資訊 (返回 JSON)
    path('api/places/<int:place_id>/', views.place_detail_api, name='place_detail_api'),

    # Ninja API 的路徑，會自動生成 /api/docs 文檔頁面
    path('api/', food_api.urls),  # food_api 是定義的 Ninja API
]
