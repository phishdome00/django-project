from django.contrib import admin
from .models import App

# Register your models here.
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'appname', 'appurl', 'user')
    list_display_links = ('id', 'appname', 'appurl', 'user')

