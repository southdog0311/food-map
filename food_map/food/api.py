from typing import List, Optional, Union
from ninja import NinjaAPI, Schema
from .models import Tag, Place
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

api = NinjaAPI()

# Schema 定義
class Tags(Schema):
    name: str
    Rstyle: Optional[str] = None

class PlaceSchema(Schema):
    name: str
    address: str
    phone_number: Optional[str] = None
    website: Optional[str] = None
    opening_time: Optional[Union[str, None]] = None
    closing_time: Optional[Union[str, None]] = None
    cuisine_type: Optional[str] = None
    menu_items: Optional[str] = None

# ===================== Tags API =====================

# 取得所有標籤
@api.get("tags", response=List[Tags])
def get_tags(request):
    tags = Tag.objects.all()
    return [{"name": tag.name, "Rstyle": tag.Rstyle} for tag in tags]

# 取得單一標籤
@api.get("tags/{tag_id}", response=Tags)
def get_tag(request, tag_id: int):
    tag = get_object_or_404(Tag, id=tag_id)
    return {"name": tag.name, "Rstyle": tag.Rstyle}

# 新增標籤
@api.post("tags")
def add_tag(request, payload: Tags):
    try:
        tag = Tag.objects.create(**payload.dict())
        return {"id": tag.id, "message": "Tag created successfully"}
    except IntegrityError:
        return {"message": "Error: Tag creation failed due to integrity error"}, 400
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500

# 更新標籤
@api.put("tags/{tag_id}")
def update_tag(request, tag_id: int, payload: Tags):
    tag = get_object_or_404(Tag, id=tag_id)
    for attr, value in payload.dict().items():
        setattr(tag, attr, value)
    tag.save()
    return {"message": "Tag updated successfully"}

# 刪除標籤
@api.delete("tags/{tag_id}")
def delete_tag(request, tag_id: int):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return {"message": "Tag deleted successfully"}

# ===================== Place API =====================

# 取得所有地點
@api.get("places", response=List[PlaceSchema])
def get_places(request):
    try:
        places = Place.objects.all()
        result = []
        for place in places:
            result.append({
                "name": place.name,
                "address": place.address,
                "phone_number": place.phone_number,
                "website": place.website,
                "opening_time": str(place.opening_time) if place.opening_time else None,
                "closing_time": str(place.closing_time) if place.closing_time else None,
                "cuisine_type": place.cuisine_type,
                "menu_items": place.menu_items
            })
        return result
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500

# 取得單一地點
@api.get("places/{place_id}", response=PlaceSchema)
def get_place(request, place_id: int):
    place = get_object_or_404(Place, id=place_id)
    return {
        "name": place.name,
        "address": place.address,
        "phone_number": place.phone_number,
        "website": place.website,
        "opening_time": str(place.opening_time) if place.opening_time else None,
        "closing_time": str(place.closing_time) if place.closing_time else None,
        "cuisine_type": place.cuisine_type,
        "menu_items": place.menu_items
    }

# 新增地點
@api.post("places")
def add_place(request, payload: PlaceSchema):
    try:
        place = Place.objects.create(**payload.dict())
        return {"id": place.id, "message": "Place created successfully"}
    except IntegrityError:
        return {"message": "Error: Place creation failed due to integrity error"}, 400
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500

# 更新地點
@api.put("places/{place_id}")
def update_place(request, place_id: int, payload: PlaceSchema):
    place = get_object_or_404(Place, id=place_id)
    for attr, value in payload.dict().items():
        setattr(place, attr, value)
    place.save()
    return {"message": "Place updated successfully"}

# 刪除地點
@api.delete("places/{place_id}")
def delete_place(request, place_id: int):
    place = get_object_or_404(Place, id=place_id)
    place.delete()
    return {"message": "Place deleted successfully"}

# ===================== search API =====================

class SearchParams(Schema):
    query: Optional[str] = None
    restaurant_name: Optional[str] = None
    cuisine_type: Optional[str] = None
    address: Optional[str] = None
    tag_ids: Optional[List[int]] = None

@api.get("search", response=List[PlaceSchema])
def search_places(request, params: SearchParams):
    try:
        search_results = Place.objects.all()

        if params.query:
            search_results = search_results.filter(name__icontains=params.query)

        if params.restaurant_name:
            search_results = search_results.filter(name__icontains=params.restaurant_name)

        if params.cuisine_type:
            search_results = search_results.filter(cuisine_type__icontains=params.cuisine_type)

        if params.address:
            search_results = search_results.filter(address__icontains=params.address)

        if params.tag_ids:
            search_results = search_results.filter(tags__id__in=params.tag_ids).distinct()

        result = []
        for place in search_results:
            result.append({
                "name": place.name,
                "address": place.address,
                "phone_number": place.phone_number,
                "website": place.website,
                "opening_time": str(place.opening_time) if place.opening_time else None,
                "closing_time": str(place.closing_time) if place.closing_time else None,
                "cuisine_type": place.cuisine_type,
                "menu_items": place.menu_items
            })
        return result
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500
