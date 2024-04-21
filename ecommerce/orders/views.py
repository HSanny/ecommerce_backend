from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    # TODO: integrate with Stripe to handle payment and then create the order instance
    
    # assume payment was successful and create dummy order

    shipping_address = request.user.shipping_address

    # Prepare the order data using the shipping address
    order_data = {
        'user': request.user.id,
        'address': shipping_address,
        'payment_details': request.data.get('payment_details'),
        'status': 'paid'  # assuming payment was successful
    }
    serializer = OrderSerializer(data=order_data)
    if serializer.is_valid():
        # Save the order to transaction_db
        with transaction.atomic(using='transaction_db'):
            order = Order(**serializer.validated_data)
            order.save(using='transaction_db')
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_order_as_received(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.status == 'received':
            order.mark_as_completed()
            return Response({'status': 'Order completed'}, status=200)
        return Response({'status': 'Order is not in received status'}, status=400)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)