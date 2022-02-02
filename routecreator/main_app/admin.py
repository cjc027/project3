from django.contrib import admin

# Register your models here.
from .models import Route, Photo, Comment, Favorite

admin.site.register(Route)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Favorite)