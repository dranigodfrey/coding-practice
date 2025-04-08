from django.contrib import admin
from .models import Job


# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'date_scraped')
    search_fields = ('title', 'company', 'description')
    list_filter = ('company', 'date_scraped')