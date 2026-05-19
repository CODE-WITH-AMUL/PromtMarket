from django.contrib import admin
from .models import Promt


@admin.register(Promt)
class PromtAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'created_at')
	search_fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}
