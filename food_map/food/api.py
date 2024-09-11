from typing import List, Optional
from ninja import NinjaAPI, Schema
from .models import Tag

api = NinjaAPI()

class Tags(Schema):
    name: str
    Rstyle: Optional[str] = None  # 將 Rstyle 欄位設為可選

@api.get("tags", response=List[Tags])
def tags(request):
    tags = Tag.objects.all()
    
    for tag in tags:
        print(tag.name, tag.Rstyle)
    return tags

@api.post("tags")
def add_tag(request, pay_load: Tags):
    tag = Tag.objects.create(**pay_load.dict())
    return {"id": tag.id}
