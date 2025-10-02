from django.db import models
from users.models import User


class Course(models.Model):
    """
    Модель учебного курса.

    Курс представляет собой обучающую программу, состоящую из одного или нескольких уроков.
    Может иметь владельца (пользователя, создавшего курс), превью, название и описание.
    """

    title = models.CharField(max_length=255, verbose_name='Название курса')
    preview = models.ImageField(
        upload_to='course_previews/',
        blank=True,
        null=True,
        verbose_name='Превью курса'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание курса'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        blank=True,
        null=True,
        verbose_name='Владелец курса'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """
    Модель урока, входящего в состав курса.

    Урок привязан к конкретному курсу и содержит название, описание,
    превью и ссылку на видео (обязательное поле).
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    title = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание урока'
    )
    preview = models.ImageField(
        upload_to='lesson_previews/',
        blank=True,
        null=True,
        verbose_name='Превью урока'
    )
    video_url = models.URLField(verbose_name='Ссылка на видео')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lessons',
        blank=True,
        null=True,
        verbose_name='Владелец урока'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'