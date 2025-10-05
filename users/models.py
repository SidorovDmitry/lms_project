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

    Каждый платёж привязан к пользователю и может относиться либо к курсу, либо к уроку
    (одно из полей course или lesson должно быть заполнено, но это не проверяется на уровне БД).
    Поддерживает два способа оплаты: наличные и банковский перевод.
    Дата платежа устанавливается автоматически при создании записи.
    """

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
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
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='TRANSFER',
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'