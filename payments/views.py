from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from materials.models import Course

from payments.services import create_stripe_product, create_stripe_price, create_checkout_session
from users.models import Payment
from drf_spectacular.utils import extend_schema, OpenApiParameter


class CreatePaymentAPIView(APIView):

    @extend_schema(
        summary="Создание платежной сессии Stripe для курса",
        description="Создает продукт, цену и сессию оплаты Stripe для указанного курса. Возвращает URL для оплаты и ID сессии.",
        parameters=[
            OpenApiParameter(
                name="course_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID курса, для которого создается платежная сессия.",
                required=True
            )
        ],
        request=None,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "payment_url": {"type": "string", "description": "URL для оплаты в Stripe."},
                    "session_id": {"type": "string", "description": "ID сессии Stripe."},
                    "amount": {"type": "integer", "description": "Сумма к оплате (в центах)."},
                    "course": {"type": "string", "description": "Название курса."}
                },
                "example": {
                    "payment_url": "https://checkout.stripe.com/...",
                    "session_id": "cs_test_...",
                    "amount": 10000,
                    "course": "Название курса"
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Курс не найден"}
                }
            }
        }
    )
    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        product = create_stripe_product(course)
        price = create_stripe_price(course.price, product.id)
        payment_url, session_id = create_checkout_session(price.id)

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=int(course.price * 100),  # предполагается, что course.price — в долларах
            session_id=session_id,
            payment_url=payment_url,
            payment_method='TRANSFER',
            status='created'
        )

        return Response({
            "payment_url": payment_url,
            "session_id": session_id,
            "amount": payment.amount,
            "course": course.title
        }, status=status.HTTP_201_CREATED)