from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from payments.views import CreatePaymentAPIView
from users.views import PaymentViewSet, RegisterView, MyTokenObtainPairView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Авторизация и регистрация
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', MyTokenObtainPairView.as_view(), name='login'),

    # Маршруты материалов
    path('api/materials/', include('materials.urls')),

    # Платежи
    path('api/payments/', include(router.urls)),

    # Документация через drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/payments/course/<int:course_id>/', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('courses/<int:course_id>/pay/', CreatePaymentAPIView.as_view(), name='course-pay'),
]
