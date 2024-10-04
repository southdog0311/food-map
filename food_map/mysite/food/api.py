from typing import List, Optional, Union
from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from .models import Tag, Place
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from ninja.security import HttpBearer

api = NinjaAPI()

# Schema 定義
class Tags(Schema):
    id: int  # 添加 id 欄位
    name: str

class PlaceSchema(Schema):
    name: str
    address: str
    phone_number: Optional[str] = None
    website: Optional[str] = None
    opening_time: Optional[str] = None  # 修改為字符串類型
    closing_time: Optional[str] = None  # 修改為字符串類型
    cuisine_type: Optional[str] = None
    menu_items: Optional[str] = None
    tags: List[Tags] = []  # 包含標籤的列表

# 自定義的 Bearer Token 認證類
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":  # 替換為你的實際 token
            return token
        return None

# 統一的錯誤處理函數
def handle_exception(e):
    raise HttpError(500, f"Error: {str(e)}")

# ===================== Tags API =====================

@api.get("tags", response=List[Tags])
def get_tags(request):
    try:
        tags = Tag.objects.all()
        return [Tags(id=tag.id, name=tag.name) for tag in tags]  # 返回 ID
    except Exception as e:
        return handle_exception(e)

@api.get("tags/{tag_id}", response=Tags)
def get_tag(request, tag_id: int):
    try:
        tag = get_object_or_404(Tag, id=tag_id)
        return Tags(id=tag.id, name=tag.name)  # 返回 ID
    except Exception as e:
        return handle_exception(e)

@api.post("/tags", auth=AuthBearer(), response=Tags)
def add_tag(request, tag: Tags):
    try:
        new_tag = Tag.objects.create(**tag.dict(exclude_unset=True))  # 只使用提供的數據
        return Tags(id=new_tag.id, name=new_tag.name)  # 返回 ID
    except IntegrityError:
        return {"message": "Error: Tag creation failed due to integrity error"}, 400
    except Exception as e:
        return handle_exception(e)

@api.put("tags/{tag_id}", auth=AuthBearer(), response=Tags)
def update_tag(request, tag_id: int, payload: Tags):
    try:
        tag = get_object_or_404(Tag, id=tag_id)
        for attr, value in payload.dict(exclude_unset=True).items():  # 僅更新提供的屬性
            setattr(tag, attr, value)
        tag.save()
        return Tags(id=tag.id, name=tag.name)  # 返回 ID
    except Exception as e:
        return handle_exception(e)

@api.delete("tags/{tag_id}", auth=AuthBearer())
def delete_tag(request, tag_id: int):
    try:
        tag = get_object_or_404(Tag, id=tag_id)
        tag.delete()
        return {"message": "Tag deleted successfully"}
    except Exception as e:
        return handle_exception(e)

# ===================== Place API =====================

@api.get("places", response=List[PlaceSchema])
def get_places(request):
    try:
        places = Place.objects.all()
        return [create_place_schema(place) for place in places]
    except Exception as e:
        return handle_exception(e)

@api.get("places/{place_id}", response=PlaceSchema)
def get_place(request, place_id: int):
    try:
        place = get_object_or_404(Place, id=place_id)
        return create_place_schema(place)
    except Exception as e:
        return handle_exception(e)

@api.post("places", response=PlaceSchema)
def add_place(request, payload: PlaceSchema):
    try:
        # 確保 opening_time 和 closing_time 為字符串
        payload.opening_time = str(payload.opening_time) if payload.opening_time else None
        payload.closing_time = str(payload.closing_time) if payload.closing_time else None
        place = Place.objects.create(**payload.dict(exclude_unset=True))
        return create_place_schema(place)
    except IntegrityError:
        return {"message": "Error: Place creation failed due to integrity error"}, 400
    except Exception as e:
        return handle_exception(e)

@api.put("places/{place_id}", response=PlaceSchema)
def update_place(request, place_id: int, payload: PlaceSchema):
    try:
        place = get_object_or_404(Place, id=place_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            # 確保 opening_time 和 closing_time 為字符串
            if attr in ['opening_time', 'closing_time']:
                value = str(value) if value else None
            setattr(place, attr, value)
        place.save()
        return create_place_schema(place)
    except Exception as e:
        return handle_exception(e)

@api.delete("places/{place_id}")
def delete_place(request, place_id: int):
    try:
        place = get_object_or_404(Place, id=place_id)
        place.delete()
        return {"message": "Place deleted successfully"}
    except Exception as e:
        return handle_exception(e)

def create_place_schema(place):
    return PlaceSchema(
        name=place.name,
        address=place.address,
        phone_number=place.phone_number,
        website=place.website,
        opening_time=place.opening_time.isoformat() if place.opening_time else None,
        closing_time=place.closing_time.isoformat() if place.closing_time else None,
        cuisine_type=place.cuisine_type,
        menu_items=place.menu_items,
        tags=[Tags(id=tag.id, name=tag.name) for tag in place.tags.all()],  # 取出標籤
    )



class VisitNum(Schema):
    today: int
    total: int

@api.get("/num_visits", response=VisitNum)
def visit_number(request):
    today_date = date.today().isoformat()
    if 'visit_dates' not in request.session:
        request.session['visit_dates'] = {}
    
    visit_dates = request.session['visit_dates']
    visit_dates[today_date] = visit_dates.get(today_date, 0) + 1
    request.session['visit_dates'] = visit_dates
    
    total_visits = sum(visit_dates.values())
    today_visits = visit_dates[today_date]
    
    return VisitNum(today=today_visits, total=total_visits)