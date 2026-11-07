from django.contrib import admin
from blog.models import post,Profile

@admin.register(post)
class postAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'date_posted','content')




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'image')