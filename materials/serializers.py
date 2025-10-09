from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson.
    Предоставляет данные об отдельном уроке, включая его связь с курсом.
    Поле 'course' содержит ID связанного курса (только для чтения по умолчанию)."""

    video_url = serializers.URLField(validators=[VideoUrlValidator])

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Course. """

    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'is_subscribed', 'lessons_count']

    def get_is_subscribed(self, obj):
        """ Определяет, подписан ли текущий пользователь на данный курс."""

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с данным курсом."""

        return obj.lessons.count()