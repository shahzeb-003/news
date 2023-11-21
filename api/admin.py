from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, News, Comment

admin.site.register(CustomUser, UserAdmin)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('title',)  # Optional: enable searching by title

admin.site.register(Comment)
