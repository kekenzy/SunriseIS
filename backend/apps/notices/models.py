from django.db import models
from django.conf import settings


class Notice(models.Model):
    TARGET_ALL = 'all'
    TARGET_PARENT = 'parent'
    TARGET_ADMIN = 'admin'
    TARGET_CHOICES = [
        (TARGET_ALL, '全員'),
        (TARGET_PARENT, '保護者'),
        (TARGET_ADMIN, '管理者・教職員'),
    ]

    title_ja = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    body_ja = models.TextField()
    body_en = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    target_role = models.CharField(max_length=10, choices=TARGET_CHOICES, default=TARGET_ALL)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_notices'
    )
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title_ja


class NoticeRead(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='reads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notice_reads')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('notice', 'user')
