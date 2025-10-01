from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для управления курсами.
    Предоставляет полный набор операций CRUD (создание, чтение, обновление, удаление)
    для модели Course."""


    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """ Представление для отображения списка уроков и создания нового урока. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ Представление для получения, обновления и удаления отдельного урока. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer