from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User, Parent, Child
from apps.billing.models import Bill, Receipt
import datetime


class BillingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent1', email='parent1@test.com',
            password='testpass123', role='parent'
        )
        self.other_user = User.objects.create_user(
            username='parent2', email='parent2@test.com',
            password='testpass123', role='parent'
        )
        self.admin_user = User.objects.create_user(
            username='admin1', email='admin1@test.com',
            password='testpass123', role='admin', is_staff=True
        )
        self.parent = Parent.objects.create(user=self.parent_user, name_ja='テスト保護者')
        other_parent = Parent.objects.create(user=self.other_user, name_ja='他の保護者')

        self.unpaid_bill = Bill.objects.create(
            parent=self.parent, month='2026-07',
            description_ja='月謝', amount=48000, status='unpaid',
            due_date=datetime.date(2026, 7, 31)
        )
        self.paid_bill = Bill.objects.create(
            parent=self.parent, month='2026-06',
            description_ja='月謝', amount=48000, status='paid',
            due_date=datetime.date(2026, 6, 30)
        )
        Receipt.objects.create(bill=self.paid_bill)
        # 他の保護者の請求
        Bill.objects.create(parent=other_parent, month='2026-07', description_ja='月謝', amount=48000, status='unpaid')

    def test_parent_sees_only_own_bills(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.get(reverse('parent-bills'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_pay_bill(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-bill-pay', args=[self.unpaid_bill.id]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], 'paid')
        self.unpaid_bill.refresh_from_db()
        self.assertEqual(self.unpaid_bill.status, 'paid')
        self.assertTrue(Receipt.objects.filter(bill=self.unpaid_bill).exists())

    def test_cannot_pay_already_paid(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-bill-pay', args=[self.paid_bill.id]))
        self.assertEqual(res.status_code, 404)

    def test_receipt_available_after_payment(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.get(reverse('parent-receipt', args=[self.paid_bill.id]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['bill']['id'], self.paid_bill.id)

    def test_admin_can_view_all_bills(self):
        self.client.force_authenticate(user=self.admin_user)
        res = self.client.get(reverse('admin-bills'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 3)

    def test_parent_cannot_access_admin_bills(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.get(reverse('admin-bills'))
        self.assertEqual(res.status_code, 403)
