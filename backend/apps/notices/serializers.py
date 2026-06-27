from rest_framework import serializers
from .models import Notice, NoticeRead


class NoticeSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'id', 'title_ja', 'title_en', 'body_ja', 'body_en',
            'is_important', 'target_role', 'published_at',
            'is_read', 'created_by_name'
        ]

    def get_is_read(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        return obj.reads.filter(user=request.user).exists()

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return ''


class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title_ja', 'title_en', 'body_ja', 'body_en', 'is_important', 'target_role']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
