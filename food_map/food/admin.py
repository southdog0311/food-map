from django.contrib import admin
from .models import  Place, Tag, TagManagement

admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(TagManagement)
