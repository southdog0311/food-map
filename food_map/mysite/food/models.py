from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=10, help_text='Enter the tag name')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Place(models.Model):
    name = models.CharField(max_length=20, help_text='Enter the name of the store')
    address = models.CharField(max_length=50, null=True, help_text='Enter the store address')
    pub_date = models.DateTimeField('date published', auto_now_add=True)  # 自動設置為當前時間
    phone_number = models.CharField(max_length=15, null=True, help_text='Enter the phone number')
    website = models.URLField(max_length=200, null=True, help_text='Enter the website URL')
    opening_time = models.TimeField(null=True, help_text='Enter the opening time')
    closing_time = models.TimeField(null=True, help_text='Enter the closing time')
    cuisine_type = models.CharField(max_length=50, null=True, help_text='Enter the type of cuisine')
    menu_items = models.TextField(null=True, help_text='Enter the menu items')
    photo_url = models.URLField(max_length=500, null=True, blank=True, help_text='Enter the photo URL')
    tags = models.ManyToManyField(Tag, related_name='places', blank=True)  # 允許空標籤
    view_count = models.PositiveIntegerField(default=0, help_text='Enter the number of views')  # 新增欄位

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TagManagement(models.Model):
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, help_text='Select a place for this tag')
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, help_text='Select a tag for this place')

    def __str__(self):
        place_name = self.place.name if self.place else 'Unknown Place'
        tag_name = self.tag.name if self.tag else 'Unknown Tag'
        return f'{place_name} - {tag_name}'

    class Meta:
        ordering = ['place']


class HomePageView(models.Model):
    viewed_at = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the homepage was viewed')

    def __str__(self):
        return f"HomePageView at {self.viewed_at}"


