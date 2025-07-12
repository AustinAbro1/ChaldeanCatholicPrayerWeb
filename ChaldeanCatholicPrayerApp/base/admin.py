from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Comment, userProfile

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(userProfile)
