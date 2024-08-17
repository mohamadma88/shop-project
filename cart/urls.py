from django.urls import path
from .views import CartView,CartAdd,CartDelete,OrderDetail,OrderCreation,ApplyDiscount,SendRequest,verify

app_name = 'cart'
urlpatterns = [
    path('cart/',CartView.as_view(), name='cart'),
    path('add/<int:pk>', CartAdd.as_view(), name='cart_add'),
    path('delete/<str:id>', CartDelete.as_view(), name='cart_delete'),
    path('order/<int:pk>', OrderDetail.as_view(), name='order_detail'),
    path('order/create', OrderCreation.as_view(), name='order_create'),
    path('discount/<int:pk>', ApplyDiscount.as_view(), name='discount'),
    path('send/<int:pk>', SendRequest.as_view(), name='send_request_pay'),
    path('verify/', verify, name='verify'),
]