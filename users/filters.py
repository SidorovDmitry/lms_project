import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """
    Фильтр для модели Payment.

    Позволяет фильтровать платежи по следующим критериям:
    - ID курса (через параметр `course`);
    - ID урока (через параметр `lesson`);
    - Способу оплаты (через параметр `payment_method`).

    Используется в API для гибкой выборки платежей, например:
        GET /payments/?course=5&payment_method=TRANSFER
    """

    # Фильтрация по курсу: принимает ID курса
    course = django_filters.NumberFilter(field_name='course__id', label='ID курса')

    # Фильтрация по уроку: принимает ID урока
    lesson = django_filters.NumberFilter(field_name='lesson__id', label='ID урока')

    # Фильтрация по способу оплаты с использованием предопределённых вариантов из модели
    payment_method = django_filters.ChoiceFilter(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        label='Способ оплаты'
    )

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']