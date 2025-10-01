from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson.
    Предоставляет данные об отдельном уроке, включая его связь с курсом.
    Поле 'course' содержит ID связанного курса (только для чтения по умолчанию)."""

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.


    """

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'lessons', 'lessons_count']

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с данным курсом."""

        return obj.lessons.count()