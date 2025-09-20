from django.contrib import admin

from .models import Petition


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

# Register your models here.
admin.site.register(Petition)