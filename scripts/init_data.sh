#!/bin/bash
# 初期データ（フィクスチャ）投入スクリプト
set -e

echo ">>> マイグレーション実行..."
docker compose exec backend python manage.py migrate

echo ">>> デモユーザー作成..."
docker compose exec backend python manage.py shell -c "
from apps.accounts.models import User, Parent, Child
from apps.dashboard.models import Event
from apps.notices.models import Notice
from django.utils import timezone

# 保護者ユーザー
if not User.objects.filter(email='parent@example.com').exists():
    parent_user = User.objects.create_user(
        username='tanaka_parent',
        email='parent@example.com',
        password='demo1234',
        role='parent',
        language='ja',
    )
    parent = Parent.objects.create(
        user=parent_user,
        name_ja='田中 花子',
        name_en='Hanako Tanaka',
        phone='090-0000-0001',
    )
    Child.objects.create(
        parent=parent,
        name_ja='田中 えま',
        name_en='Emma Tanaka',
        class_name='Sunflower',
        enrolled_at='2024-04-01',
    )
    print('  ✓ 保護者ユーザー作成: parent@example.com / demo1234')

# 管理者ユーザー
if not User.objects.filter(email='admin@example.com').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin1234',
        role='admin',
    )
    print('  ✓ 管理者ユーザー作成: admin@example.com / admin1234')
else:
    admin_user = User.objects.get(email='admin@example.com')

# イベント
if not Event.objects.exists():
    Event.objects.create(title_ja='夏祭り', title_en='Summer Festival', event_date='2026-07-12', time_range='10:00-14:00', place='グラウンド')
    Event.objects.create(title_ja='保護者面談', title_en='Parent-Teacher Meeting', event_date='2026-07-20', time_range='13:00-17:00', place='各教室')
    print('  ✓ イベントデータ作成')

# お知らせ
if not Notice.objects.exists():
    Notice.objects.create(title_ja='7月の月謝請求を発行しました', title_en='July tuition invoice issued', body_ja='7月分の月謝請求書を発行いたしました。', body_en='July tuition invoice has been issued.', is_important=True, target_role='parent', created_by=admin_user)
    Notice.objects.create(title_ja='夏祭りの参加可否をご回答ください', title_en='Please RSVP for the Summer Festival', body_ja='7月12日(土)に夏祭りを開催します。参加可否をご回答ください。', body_en='Please RSVP for the Summer Festival on July 12.', is_important=False, target_role='parent', created_by=admin_user)
    Notice.objects.create(title_ja='健康診断の結果を掲載しました', title_en='Health check results posted', body_ja='5月に実施した健康診断の結果を掲載しました。', body_en='May health check results have been posted.', is_important=False, target_role='all', created_by=admin_user)
    print('  ✓ お知らせデータ作成')

# 請求データ（Phase 2）
from apps.billing.models import Bill, Receipt
import datetime
if not Bill.objects.exists():
    try:
        parent_obj = Parent.objects.get(user__email='parent@example.com')
        bills = [
            Bill(parent=parent_obj, month='2026-07', description_ja='月謝', description_en='Tuition', amount=48000, status='unpaid', due_date='2026-07-31'),
            Bill(parent=parent_obj, month='2026-06', description_ja='月謝', description_en='Tuition', amount=48000, status='paid', due_date='2026-06-30'),
            Bill(parent=parent_obj, month='2026-05', description_ja='月謝＋教材費', description_en='Tuition + Materials', amount=52000, status='paid', due_date='2026-05-31'),
            Bill(parent=parent_obj, month='2026-04', description_ja='入学関連費用', description_en='Enrollment Fee', amount=120000, status='paid', due_date='2026-04-30'),
        ]
        for b in bills:
            b.save()
            if b.status == 'paid':
                Receipt.objects.create(bill=b)
        print('  ✓ 請求データ作成')
    except Parent.DoesNotExist:
        pass

# 申請・アンケートデータ（Phase 2）
from apps.events.models import Submission, Survey
if not Submission.objects.exists():
    try:
        parent_obj = Parent.objects.get(user__email='parent@example.com')
        Submission.objects.create(parent=parent_obj, title_ja='健康調査票（年次）', title_en='Annual Health Survey', due_date='2026-06-30', status='pending')
        Submission.objects.create(parent=parent_obj, title_ja='夏季預かり保育 申込', title_en='Summer Care Application', due_date='2026-07-05', status='pending')
        Submission.objects.create(parent=parent_obj, title_ja='食物アレルギー申告', title_en='Food Allergy Declaration', due_date='2026-05-12', status='accepted')
        print('  ✓ 申請データ作成')
    except Parent.DoesNotExist:
        pass

if not Survey.objects.exists():
    Survey.objects.create(
        title_ja='運動会の開催時期について',
        title_en='Sports Day Timing Survey',
        options_ja=['春（4〜5月）', '秋（10〜11月）', 'どちらでも'],
        options_en=['Spring (Apr-May)', 'Fall (Oct-Nov)', 'Either is fine'],
    )
    print('  ✓ アンケートデータ作成')

print('>>> 初期データ投入完了')
"

echo ""
echo "=== ログイン情報 ==="
echo "保護者: parent@example.com / demo1234"
echo "管理者: admin@example.com / admin1234"
