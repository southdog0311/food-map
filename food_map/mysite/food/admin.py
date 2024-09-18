from django.contrib import admin
from .models import Place, Tag, TagManagement

class TagInlineAdmin(admin.StackedInline):
    model = Place.tags.through

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'website', 'pub_date')
    list_filter = ('pub_date', 'tags')
    search_fields = ('name', 'address', 'website')
    ordering = ('-id',)
    readonly_fields = ('pub_date',)
    inlines = [TagInlineAdmin]

admin.site.register(Tag)
admin.site.register(Place, PlaceAdmin)
admin.site.register(TagManagement)
