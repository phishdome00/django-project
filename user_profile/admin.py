from django.contrib import admin
from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_fk', 'phone_no', 'user_type', 'slug','created_at')
    list_display_links = ('id', 'user_fk', 'slug')

