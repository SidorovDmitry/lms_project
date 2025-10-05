from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Payment

User = get_user_model()


# Сериализатор для отображения и редактирования профиля пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']
        read_only_fields = ['id']


# Сериализатор регистрации нового пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'city']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        validated_data.pop('avatar', None)
        user = User.objects.create_user(**validated_data)
        return user


# Сериализатор входа (логин по email и паролю)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Требуется email и пароль")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Неверные учетные данные")

        data['user'] = user
        return data


# Сериализатор платежей
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
