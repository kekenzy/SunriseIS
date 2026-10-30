from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent = User.objects.create_user(
            username='parent1', email='parent1@test.com',
            password='testpass123', role='parent'
        )
        self.admin = User.objects.create_user(
            username='admin1', email='admin1@test.com',
            password='testpass123', role='admin', is_staff=True
        )

    def test_login_success(self):
        from unittest.mock import patch, MagicMock
        from rest_framework.response import Response as DRFResponse
        mock_tokens = {'access': 'mock-access', 'refresh': 'mock-refresh'}
        mock_response = DRFResponse(mock_tokens, status=200)
        with patch('apps.accounts.views.LoginView.post', return_value=mock_response):
            res = self.client.post(reverse('login'), {
                'email': 'parent1@test.com', 'password': 'testpass123'
            })
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_login_wrong_password(self):
        res = self.client.post(reverse('login'), {
            'email': 'parent1@test.com', 'password': 'wrongpass'
        })
        self.assertEqual(res.status_code, 401)

    def test_login_locks_after_repeated_failures(self):
        from unittest.mock import patch
        from django.core.cache import cache
        from rest_framework.throttling import ScopedRateThrottle
        cache.clear()
        # IP 単位の制限は切り、ログインID単位のロックだけを確認する
        with patch.object(ScopedRateThrottle, 'allow_request', return_value=True):
            for _ in range(10):
                res = self.client.post(reverse('login'), {'email': 'parent1@test.com', 'password': 'wrongpass'})
                self.assertEqual(res.status_code, 401)
            res = self.client.post(reverse('login'), {'email': 'parent1@test.com', 'password': 'testpass123'})
        self.assertEqual(res.status_code, 429)
        cache.clear()

    def test_me_requires_auth(self):
        res = self.client.get(reverse('me'))
        self.assertEqual(res.status_code, 401)

    def test_me_returns_user(self):
        self.client.force_authenticate(user=self.parent)
        res = self.client.get(reverse('me'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'], 'parent1@test.com')
        self.assertEqual(res.data['role'], 'parent')

    def test_logout_blacklists_token(self):
        from unittest.mock import patch, MagicMock
        mock_token = MagicMock()
        self.client.force_authenticate(user=self.parent)
        with patch('apps.accounts.views.RefreshToken', return_value=mock_token):
            res = self.client.post(reverse('logout'), {'refresh': 'mock-refresh-token'})
        self.assertEqual(res.status_code, 200)
        mock_token.blacklist.assert_called_once()
