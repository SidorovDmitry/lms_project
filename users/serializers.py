from rest_framework import serializers
from .models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя (User).

    Используется для преобразования данных пользователя в JSON и обратно.
    Включает основные профильные поля: email, телефон, город и аватар.
    Поле 'id' включено для идентификации объекта.

    Пароль и другие чувствительные данные намеренно исключены из сериализации
    в целях безопасности.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели платежа (Payment).

    Предоставляет полное представление платежа, включая пользователя,
    оплаченный курс или урок, сумму, способ и дату оплаты.

    Использует все поля модели (fields = '__all__'), что удобно для
    внутреннего API или админских целей. В публичном API рекомендуется
    явно указывать нужные поля и скрывать чувствительную информацию.
    """

    class Meta:
        model = Payment
        fields = '__all__'