from django.contrib import admin
from .models import Violation

# Register your models here.
@admin.register(Violation)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'title', 'app', 'date')
    list_display_links = ('id', 'url', 'title', 'app')

