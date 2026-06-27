from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_PARENT = 'parent'
    ROLE_ADMIN = 'admin'
    ROLE_STAFF = 'staff'
    ROLE_CHOICES = [
        (ROLE_PARENT, '保護者'),
        (ROLE_ADMIN, '管理者'),
        (ROLE_STAFF, '教職員'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_PARENT)
    language = models.CharField(max_length=2, default='ja', choices=[('ja', '日本語'), ('en', 'English')])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_admin_or_staff(self):
        return self.role in (self.ROLE_ADMIN, self.ROLE_STAFF)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    name_ja = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name_ja


class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    name_ja = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True)
    class_name = models.CharField(max_length=50)
    enrolled_at = models.DateField()

    def __str__(self):
        return self.name_ja
