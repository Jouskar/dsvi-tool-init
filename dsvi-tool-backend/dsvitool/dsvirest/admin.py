from django.contrib import admin
from .models import Dataset


# Register your models here.
@admin.register(Dataset)
class AuthorAdmin(admin.ModelAdmin):
    pass
