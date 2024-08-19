from django.db import models

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

    def __str__(self):
        return self.name
