from django.contrib import admin
from . import  models

# Register your models here.
admin.site.register(models.Seller)
admin.site.register(models.Broker)
admin.site.register(models.Apartment)
admin.site.register(models.Image)
admin.site.register(models.Inquiries)

