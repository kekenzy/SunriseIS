from django.contrib import admin
from .models import Notice, NoticeRead


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title_ja', 'is_important', 'target_role', 'published_at']
    list_filter = ['is_important', 'target_role']
    search_fields = ['title_ja', 'title_en']


@admin.register(NoticeRead)
class NoticeReadAdmin(admin.ModelAdmin):
    list_display = ['notice', 'user', 'read_at']
