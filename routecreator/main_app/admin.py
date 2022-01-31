from django.contrib import admin

# Register your models here.
from .models import Route, Photo

admin.site.register(Route)
admin.site.register(Photo)