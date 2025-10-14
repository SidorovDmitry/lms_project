from drf_spectacular.utils import extend_schema_serializer
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
        read_only_fields = ['owner']

@ extend_schema_serializer(exclude_fields=['is_subscribed', 'lessons_count'])
class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Course. """

    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    stripe_product_id = serializers.CharField(read_only=True)
    stripe_price_id = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'is_subscribed', 'lessons_count','lessons', 'stripe_price_id', 'stripe_product_id']
        read_only_fields = ['owner', 'stripe_product_id', 'stripe_price_id']

    def get_is_subscribed(self, obj):
        """ Определяет, подписан ли текущий пользователь на данный курс."""

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с данным курсом."""

        return obj.lessons.count()