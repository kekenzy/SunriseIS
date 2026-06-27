from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User, Parent, Child
from apps.notices.models import Notice, NoticeRead
import datetime


class NoticeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent1', email='parent1@test.com',
            password='testpass123', role='parent'
        )
        self.admin_user = User.objects.create_user(
            username='admin1', email='admin1@test.com',
            password='testpass123', role='admin', is_staff=True
        )
        parent = Parent.objects.create(user=self.parent_user, name_ja='テスト保護者')
        Child.objects.create(parent=parent, name_ja='テスト子', class_name='A', enrolled_at=datetime.date.today())

        self.notice_all = Notice.objects.create(
            title_ja='全員向けお知らせ', body_ja='本文', target_role='all', created_by=self.admin_user
        )
        self.notice_parent = Notice.objects.create(
            title_ja='保護者向けお知らせ', body_ja='本文', target_role='parent', created_by=self.admin_user
        )
        self.notice_admin = Notice.objects.create(
            title_ja='管理者向けお知らせ', body_ja='本文', target_role='admin', created_by=self.admin_user
        )

    def test_parent_can_see_all_and_parent_notices(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.get(reverse('parent-notices'))
        self.assertEqual(res.status_code, 200)
        titles = [n['title_ja'] for n in res.data]
        self.assertIn('全員向けお知らせ', titles)
        self.assertIn('保護者向けお知らせ', titles)
        self.assertNotIn('管理者向けお知らせ', titles)

    def test_parent_notice_detail_marks_read(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.get(reverse('parent-notice-detail', args=[self.notice_all.id]))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(NoticeRead.objects.filter(notice=self.notice_all, user=self.parent_user).exists())

    def test_admin_can_create_notice(self):
        self.client.force_authenticate(user=self.admin_user)
        res = self.client.post(reverse('admin-notices'), {
            'title_ja': '新しいお知らせ', 'body_ja': '内容',
            'target_role': 'all', 'is_important': False
        })
        self.assertEqual(res.status_code, 201)

    def test_parent_cannot_create_notice(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('admin-notices'), {
            'title_ja': '不正', 'body_ja': '内容', 'target_role': 'all'
        })
        self.assertEqual(res.status_code, 403)

    def test_unauthenticated_cannot_access_notices(self):
        res = self.client.get(reverse('parent-notices'))
        self.assertEqual(res.status_code, 401)
