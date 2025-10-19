from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator,IsOwnerOrModeratorReadOnly
from .tasks import check_and_notify_subscribers


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для управления курсами.
    Предоставляет полный набор операций CRUD (создание, чтение, обновление, удаление)
    для модели Course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """ Проверка прав доступа. """
        if self.action == 'create':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Не модератор может создать
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrModeratorReadOnly]  # Модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrModeratorReadOnly]  # Удалить может только владелец
        return super().get_permissions()

    def perform_create(self, serializer):
        """Cоздание курса и привязка владельца."""
        serializer.save(owner=self.request.user)  # Привязка к владельцу

    def perform_update(self, serializer):
        """Обновление курса и рассылка уведомлений подписчикам."""
        course = serializer.save()
        check_and_notify_subscribers.deley(course.id)


class LessonListCreateView(generics.ListCreateAPIView):
    """ Представление для отображения списка уроков и создания нового урока. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """ Проверка прав доступа. """
        if self.request.method == 'POST':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Создание — не модератор
        return super().get_permissions()

    def perform_create(self, serializer):
        """Привязка владельца и курса к уроку."""
        course_id = self.kwargs.get('course_id') or self.request.data.get('course')

        if not course_id:
            raise serializers.ValidationError({"course": "Не указан course"})

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": "Курс не найден"})

        serializer.save(owner=self.request.user, course=course)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ Представление для получения, обновления и удаления отдельного урока. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModeratorReadOnly]  # Редактирование и просмотр: владелец или модератор

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        


class SubscriptionAPIView(APIView):
    """Представление для управления подпиской пользователя на курс."""

    @extend_schema(
        summary="Управление подпиской на курс",
        description="Добавляет или удаляет подписку пользователя на указанный курс",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'course_id': {
                        'type': 'integer',
                        'description': 'ID курса для подписки/отписки',
                        'example': 1
                    }
                },
                'required': ['course_id']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Сообщение о результате операции',
                        'examples': [
                            'подписка добавлена',
                            'подписка удалена'
                        ]
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Сообщение об ошибке',
                        'examples': [
                            'Не указан course_id',
                            'Курс не найден'
                        ]
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                'Пример успешной подписки',
                value={'message': 'подписка добавлена'},
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Пример успешной отписки',
                value={'message': 'подписка удалена'},
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Пример ошибки',
                value={'error': 'Курс не найден'},
                response_only=True,
                status_codes=['400']
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Не указан course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course_item = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Курс не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)