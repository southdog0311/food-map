from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=10)
    Rstyle = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Place(models.Model):
    name = models.CharField(max_length=20, help_text='Enter the name of store')
    address = models.CharField(max_length=50, null=True)
    pub_date = models.DateTimeField('date published')
    phone_number = models.CharField(max_length=15, null=True, help_text='Enter the phone number')
    website = models.URLField(max_length=200, null=True, help_text='Enter the website URL')
    opening_time = models.TimeField(null=True, help_text='Enter the opening time')
    closing_time = models.TimeField(null=True, help_text='Enter the closing time')
    cuisine_type = models.CharField(max_length=50, null=True, help_text='Enter the type of cuisine')
    menu_items = models.TextField(null=True, help_text='Enter the menu items')
    photo_url = models.URLField(max_length=500, null=True, blank=True, help_text='Enter the photo URL')
    tags = models.ManyToManyField(Tag, related_name='places') 

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    

class TagManagement(models.Model):
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        place_name = self.place.name if self.place else 'Unknown Place'
        tag_name = self.tag.name if self.tag else 'Unknown Tag'
        return f'{place_name} - {tag_name}'
    
    class Meta:
        ordering = ['place']