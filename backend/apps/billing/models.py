from django.db import models
from apps.accounts.models import Parent


class Bill(models.Model):
    STATUS_UNPAID = 'unpaid'
    STATUS_PAID = 'paid'
    STATUS_CHOICES = [
        (STATUS_UNPAID, '未払い'),
        (STATUS_PAID, '支払済'),
    ]

    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='bills')
    month = models.CharField(max_length=7)  # "2026-07"
    description_ja = models.CharField(max_length=200)
    description_en = models.CharField(max_length=200, blank=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_UNPAID)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month']

    def __str__(self):
        return f"{self.parent} - {self.month} - ¥{self.amount}"


class Receipt(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name='receipt')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"領収書: {self.bill}"
