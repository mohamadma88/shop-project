from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import View
from account.models import Address
from product.models import Product
from .cart_module import Cart
from .models import Order, OrderItem, DiscountCode
from django.conf import settings
import requests
import json


# Display cart
class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})


# Add product to cart
class CartAdd(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get('size', 'empty'), request.POST.get('color', 'empty'), request.POST.get(
            'quantity')
        cart = Cart(request)
        cart.add(product, color, size, quantity)

        return redirect('cart:cart')

# Remove the selected product from the shopping cart
class CartDelete(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart')

# order detail
class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/cart_detail.html', {'order': order})

# order detail
class OrderCreation(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)

        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     size=item['size'], color=item['color'], quantity=item['quantity'], )

            cart.remove_cart()
            return redirect('cart:order_detail', order.id)


# Creating and applying a discount code
class ApplyDiscount(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        code = request.POST.get('discount_code')
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            return redirect('cart:order_detail', order.id)
        order.total_price -= order.total_price * discount_code.discount / 100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:order_detail', order.id)

# Payment gateway page
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/cart/verify/'


class SendRequest(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        address = get_object_or_404(Address, id=request.POST.get('address'))
        order.address = f'{address.address}-{address.phone}'
        order.save()
        request.session['order_id'] = str(order.id)
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price,
            "Description": description,
            "Phone": request.user.phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                            'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


def verify(authority):
    order_id = requests.session['order_id']
    order = Order.objects.get(id=int(order_id))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.total_price,
        "Authority": authority,
    }

    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()

        if response['Status'] == 100:
            order.is_paid = True
            order.save()
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
