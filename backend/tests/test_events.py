from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User, Parent, Child
from apps.dashboard.models import Event
from apps.events.models import EventRsvp, AbsenceReport, Submission, Survey
import datetime


class EventRsvpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent1', email='parent1@test.com',
            password='testpass123', role='parent'
        )
        parent = Parent.objects.create(user=self.parent_user, name_ja='テスト保護者')
        Child.objects.create(parent=parent, name_ja='テスト子', class_name='A', enrolled_at=datetime.date.today())

        self.future_event = Event.objects.create(
            title_ja='夏祭り', event_date=datetime.date(2027, 7, 12)
        )

    def test_rsvp_attending(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-event-rsvp', args=[self.future_event.id]), {'status': 'attending'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], 'attending')

    def test_rsvp_update(self):
        EventRsvp.objects.create(event=self.future_event, user=self.parent_user, status='attending')
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-event-rsvp', args=[self.future_event.id]), {'status': 'not_attending'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], 'not_attending')
        self.assertEqual(EventRsvp.objects.filter(event=self.future_event, user=self.parent_user).count(), 1)

    def test_rsvp_invalid_status(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-event-rsvp', args=[self.future_event.id]), {'status': 'maybe'})
        self.assertEqual(res.status_code, 400)


class AbsenceReportTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent1', email='parent1@test.com',
            password='testpass123', role='parent'
        )
        parent = Parent.objects.create(user=self.parent_user, name_ja='テスト保護者')
        Child.objects.create(parent=parent, name_ja='テスト子', class_name='A', enrolled_at=datetime.date.today())

    def test_report_absence(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-absence'), {'date': '2026-07-01', 'reason': '発熱'})
        self.assertEqual(res.status_code, 201)
        self.assertTrue(AbsenceReport.objects.filter(date='2026-07-01').exists())

    def test_absence_requires_date(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-absence'), {'reason': '発熱'})
        self.assertEqual(res.status_code, 400)


class SurveyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent1', email='parent1@test.com',
            password='testpass123', role='parent'
        )
        self.survey = Survey.objects.create(
            title_ja='テストアンケート',
            options_ja=['選択肢A', '選択肢B', '選択肢C'],
        )

    def test_answer_survey(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-survey-answer', args=[self.survey.id]), {'choice_index': 1})
        self.assertEqual(res.status_code, 200)

    def test_invalid_choice_index(self):
        self.client.force_authenticate(user=self.parent_user)
        res = self.client.post(reverse('parent-survey-answer', args=[self.survey.id]), {'choice_index': 99})
        self.assertEqual(res.status_code, 400)

    def test_survey_list_shows_my_response(self):
        self.client.force_authenticate(user=self.parent_user)
        self.client.post(reverse('parent-survey-answer', args=[self.survey.id]), {'choice_index': 0})
        res = self.client.get(reverse('parent-surveys'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]['my_response'], 0)
