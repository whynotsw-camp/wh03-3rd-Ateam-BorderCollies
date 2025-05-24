from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample

from django.utils import timezone

from users.models import User
from users.serializers import (
    DailyStatusSerializer,
    UserProfileResponseSerializer,
)
from diaries.models import Diary, Emotion
from datetime import timedelta


class DailyStatusView(APIView):
    """
    API-U001: 앱 초기 사용자 상태 확인
    GET /api/users/me/daily-status/

    응답 코드:
    - 200 OK: 정상 응답
    - 401 Unauthorized: 인증 실패
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DailyStatusSerializer

    def get(self, request):
        user = request.user
        today = timezone.localdate()

        # 오늘 감정 조회
        emotion_entry = Emotion.objects.filter(user=user, date=today).first()
        emotion = emotion_entry.emotion_name if emotion_entry else None

        # 오늘 일기 존재 여부 확인
        diary_exists = Diary.objects.filter(user=user, diary_date__date=today).exists()

        data = {
            "is_authenticated": True,
            "today_date": today,
            "emotion": emotion,
            "diary_exists": diary_exists,
        }

        serializer = DailyStatusSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    API-U002: 유저 프로필 조회
    GET /api/users/me/profile/

    응답 코드:
    - 200 OK: 정상 응답
    - 401 Unauthorized: 인증 실패
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileResponseSerializer

    @extend_schema(
        description="사용자 프로필 조회", responses={200: UserProfileResponseSerializer}
    )
    def get(self, request):
        user = request.user
        # 여기서 하드코딩된 값으로 설정
        data = {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'email': user.email,
            'joined_date': timezone.localdate() - timedelta(days=60),  # 하드코딩
            'diary_count': 7,  # 하드코딩
            'last_diary_date': timezone.localdate() - timedelta(days=0)  # 하드코딩
        }
        # 디버그 메시지
        # print("User data:", data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
