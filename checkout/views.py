import decimal

from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
# from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import CreateAPIView
from addresses.models import Address
from checkout.models import Cart, CartItem, Post, Discount, Order, Payment
from checkout.serializers import CartSerializer, AddToCartSerializer, CartItemSerializer, OrderSerializer, \
    PaymentSerializer, DiscountSerializer


# class CartViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#
#
# class CartItemViewSet(ModelViewSet):
#     def get_queryset(self):
#         return CartItem.objects.filter(cart__id=self.kwargs['cart_pk'])
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return AddToCartSerializer
#         else:
#             return CartItemSerializer

class CartAPIView(APIView):
    serializer_class = CartSerializer


# class CartDetail(APIView):
#     def get(self, request, cart_id):
#         cart = Cart.objects.get(id=cart_id)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrder(APIView):
    def post(self, request):
        try:
            cart_id = request.data['cart_id']
            cart = Cart.objects.get(id=cart_id)
            post_id = request.data['post_id']
            post = Post.objects.get(id=post_id)
            address_id = request.data['address_id']
            address = Address.objects.get(id=address_id)
        except:
            response = {'message': 'some of the attributes not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            discount_code = request.data['discount_code']
            if not discount_code:
                final_price = cart.get_total_cost() + post.cost()
                order = Order.objects.create(cart=cart, post=post, address=address,
                                             final_price=final_price, status='RTP')
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                try:
                    discount = Discount.objects.get(code=discount_code)
                except:
                    response = {'message': 'invalid discount code'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    final_price = (cart.get_total_cost() * (
                            decimal.Decimal(discount.discount_percent) / 100)) + post.cost
                    order = Order.objects.create(cart=cart, post=post, discount=discount, address=address,
                                                 final_price=final_price,
                                                 status='RTP')
                    serializer = OrderSerializer(order)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreatePayment(APIView):
    def post(self, request):
        try:
            order_id = request.data['order_id']
            try:
                order = Order.objects.get(id=order_id)
            except:
                response = {'message': 'order not found'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                if not order.status == 'RTP':
                    response = {'message': 'order has already been paid'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    receipt = request.data['receipt']
                    payment_tracking_code = request.data['payment_tracking_code']
        except:
            response = {'message': 'bad data'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment = Payment.objects.create(order=order, receipt=receipt,
                                             payment_tracking_code=payment_tracking_code,
                                             type='IN', total_price=order.final_price)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def update(self, request, *args, **kwargs):
        response = {'message': 'cant edit discounts'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PATCH'], )
    def activate(self, request, pk=None):
        discount = Discount.objects.get(id=pk)
        if discount.is_active:
            response = {'message': 'discount is already activated'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            discount.is_active = True
            discount.save()
            response = {'message': 'discount activated'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'], )
    def deactivate(self, request, pk=None):
        discount = Discount.objects.get(id=pk)
        if not discount.is_active:
            response = {'message': 'discount is not activated'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            discount.is_active = False
            discount.save()
            response = {'message': 'discount deactivated'}
            return Response(response, status=status.HTTP_200_OK)


