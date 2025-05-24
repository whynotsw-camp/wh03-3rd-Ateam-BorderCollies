from rest_framework import serializers
from galleries.models import Location
from diaries.models import Diary
from .models import Event, Timeline
from django.apps import apps

Keyword = apps.get_model("events", "Keyword")
import os

### 📌 Keyword Serializer
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["content"]


### 📌 Timeline Serializer
class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['timeline_id', 'date', 'user', 'events', 'event_ids_series']


### 📌 Event Serializer
class EventSerializer(serializers.ModelSerializer):
    time = serializers.CharField()
    emotion_id = serializers.IntegerField(source="event_emotion_id")
    
    keywords = KeywordSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = [
            "event_id",
            "date",
            "time",
            "longitude",
            "latitude",
            "title",
            "emotion_id",
            "weather",
            "memo_content",  # 메인 메모 필드
            "keywords",
            "tag"
        ]
        extra_kwargs = {
            'date': {'required': True},
            'time': {'required': True},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'title': {'required': False},
            'emotion_id': {'default': 1},
            'weather': {'default': 'sunny'},
            'memo_content': {'required': False, 'allow_blank': True},
            'tag': {'required': False},
        }

    ### ✅ create(): Nested Create
    # def create(self, validated_data):
    #     memos_data = validated_data.pop('memos', [])
    #     keywords_data = validated_data.pop('keywords', [])

    #     # 이벤트 생성
    #     event = Event.objects.create(**validated_data)

    #     # 메모 생성
    #     for memo_data in memos_data:
    #         Memo.objects.create(event=event, **memo_data)

    #     # 키워드 생성
    #     for keyword_data in keywords_data:
    #         Keyword.objects.create(event=event, **keyword_data)
            

    #     # Timeline의 event_ids_series 업데이트 (event_ids_series는 ID 목록이라 가정)
    #     timeline = Timeline.objects.get(user=event.user, date=event.date)
    #     timeline.event_ids_series.append(event.event_id)
    #     timeline.save()

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        # memo_content 추출
        memo_content = validated_data.get('memo_content')
        keywords_data = validated_data.pop('keywords', [])

        # 이벤트 생성
        event = Event.objects.create(
            user=user,
            memo_content=memo_content,
            **{k: v for k, v in validated_data.items() if k != 'memo_content'}
        )

        # 키워드 생성
        for keyword_data in keywords_data:
            Keyword.objects.create(event=event, **keyword_data)
            
        # 타임라인 연결 및 업데이트
        timeline, created = Timeline.objects.get_or_create(user=user, date=event.date)
        if not hasattr(timeline, 'event_ids_series') or timeline.event_ids_series is None:
            timeline.event_ids_series = []

        timeline.event_ids_series.append(event.event_id)
        timeline.save()

        return event

    ### ✅ update(): Nested Update (전체 교체 방식)
    def update(self, instance, validated_data):
        memos_data = validated_data.pop("memos", None)
        keywords_data = validated_data.pop("keywords", None)

        # 기본 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 메모 전체 삭제 후 재등록 (단순화된 로직)
        if memos_data is not None:
            instance.memos.all().delete()
            for memo_data in memos_data:
                Memo.objects.create(event=instance, **memo_data)

        # 키워드 전체 삭제 후 재등록
        if keywords_data is not None:
            instance.keywords.all().delete()
            for keyword_data in keywords_data:
                Keyword.objects.create(event=instance, **keyword_data)

        return instance

