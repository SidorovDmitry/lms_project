from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator,IsOwnerOrModeratorReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для управления курсами.
    Предоставляет полный набор операций CRUD (создание, чтение, обновление, удаление)
    для модели Course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Не модератор может создать
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrModeratorReadOnly]  # Модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrModeratorReadOnly]  # Удалить может только владелец
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязка к владельцу


class LessonListCreateView(generics.ListCreateAPIView):
    """ Представление для отображения списка уроков и создания нового урока. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Создание — не модератор
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        serializer.save(owner=self.request.user, course=course)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ Представление для получения, обновления и удаления отдельного урока. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModeratorReadOnly]  # Редактирование и просмотр: владелец или модератор

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        

class SubscriptionAPIView(APIView):
    """ Представление для управления подпиской пользователя на курс."""

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
                status=status.HTTP_400_BAD_REQUEST  # ← Меняем сюда
            )

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
        