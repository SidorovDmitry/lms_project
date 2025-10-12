from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер для кастомной модели User с email в качестве уникального идентификатора.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email обязательно для заполнения')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    """
    Кастомная модель пользователя, использующая email в качестве основного идентификатора.

    Заменяет стандартное поле `username` на `email`, который должен быть уникальным.
    Дополнительно содержит контактную и профильную информацию: телефон, город, аватар.
    Используется как основная модель пользователя в проекте (указана в settings.AUTH_USER_MODEL).
    """

    username = None  # Отключаем поле username
    email = models.EmailField(unique=True, verbose_name='Электронная почта')

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Город'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Не требуем дополнительных полей при создании суперпользователя

    objects = CustomUserManager()

    # Переопределяем связи с группами и правами, чтобы избежать конфликтов имён
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='Группы',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='Права пользователя',
    )

    def __str__(self):
        return self.email


class Payment(models.Model):
    """
    Модель платежа за курс или отдельный урок.
    """
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счёт'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('created', 'Создано'),
        ('paid', 'Оплачено'),
        ('unpaid', 'Не оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='payments'  # Добавил related_name
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс',
        related_name='payments'  # Добавил related_name
    )
    lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок',
        related_name='payments'  # Добавил related_name
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма (в центах)',
        help_text='Сумма в центах (например, 999 = $9.99)'
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Product ID'
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Price ID'
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Session ID'
    )
    payment_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на оплату'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='TRANSFER',
        verbose_name='Способ оплаты'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='created',
        verbose_name='Статус платежа'
    )

    def clean(self):
        """Проверка, что указан либо курс, либо урок"""
        from django.core.exceptions import ValidationError
        if self.course and self.lesson:
            raise ValidationError('Платёж может быть привязан только к курсу ИЛИ уроку, но не к обоим.')
        if not self.course and not self.lesson:
            raise ValidationError('Платёж должен быть привязан к курсу или уроку.')

    @property
    def amount_in_dollars(self):
        """Возвращает сумму в долларах"""
        return self.amount / 100.0

    @property
    def is_paid(self):
        """Проверяет, оплачен ли платёж"""
        return self.status == 'paid'

    @property
    def product_name(self):
        """Возвращает название продукта (курса или урока)"""
        if self.course:
            return self.course.title
        elif self.lesson:
            return self.lesson.title
        return "Неизвестный продукт"

    def __str__(self):
        return f"{self.user} - ${self.amount_in_dollars:.2f} ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']  # Добавил сортировку по умолчанию
        indexes = [
            models.Index(fields=['user', 'payment_date']),
            models.Index(fields=['status']),
            models.Index(fields=['session_id']),
        ]