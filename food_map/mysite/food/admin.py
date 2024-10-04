from django.contrib import admin
from .models import Place, Tag, TagManagement

# 用於在 Place 的編輯頁面嵌入 Tag
class TagInlineAdmin(admin.TabularInline):
    model = Place.tags.through  # 這裡通過 Place.tags.through 來建立關聯
    extra = 1  # 顯示一個額外的空白行

# 管理 Place 的後台
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'website', 'pub_date', 'view_count')  # 顯示地點的相關資訊
    list_filter = ('pub_date', 'tags')  # 根據發佈日期和標籤過濾
    search_fields = ('name', 'address', 'website')  # 支持根據名稱、地址和網站搜尋
    ordering = ('-pub_date',)  # 依照發佈日期降序排列
    readonly_fields = ('pub_date',)  # pub_date 是唯讀的

    # 將 Tag 以 inline 形式顯示
    inlines = [TagInlineAdmin]

    # 新增批量操作
    actions = ['increase_view_count']

    def increase_view_count(self, request, queryset):
        count = queryset.count()
        for place in queryset:
            place.view_count += 1  # 將每個地點的觀看次數加 1
            place.save()  # 保存修改
        self.message_user(request, f'已成功將 {count} 個地點的觀看次數增加。')

    increase_view_count.short_description = "增加選擇地點的觀看次數"  # 行動描述

# 註冊到 Django 管理站點
admin.site.register(Tag)
admin.site.register(Place, PlaceAdmin)
admin.site.register(TagManagement)
