from django.shortcuts import render
"""
Contains the view functions or view classes for your app.
Views handle the request-response cycle for your application. They fetch data from models and pass it to templates.
"""
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer

@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # traditional way of django reg 
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('login') # redirect to login page after registration
        
    #     else:
    #         form = CustomUserCreationForm()
        
    #     return render(request, 'users/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def login_view(request):
    # Django's built-in authentication system
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            email = email,
            password = password
        )
        if user is not None:
            # token-based or session-based
            # session-based authentication for security reason
            login(request, user)
            user_data = CustomUserSerializer(user).data
            orders = Order.objects.using('transaction_db').filter(user=user)
            orders_data = OrderSerializer(orders, many=True).data
            return JsonResponse({
                "message": "Login Successfully",
                "userData": user_data,
                "transactionData": orders_data
            }, status=200)

        else:
            return JsonResponse(
                {"error": "Invalid credentials"},
                status=401
            )
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except CartItem.DoesNotExist:
        return Response({'message': 'Item not found'}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        return Response({'message': 'Item removed successfully'}, status=204)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return Response({'message': 'Cart cleared successfully'}, status=204)