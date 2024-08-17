from django.urls import path
from .views import NavBar, ProductList, searchview, product_detail

app_name = 'product'

urlpatterns = [
    path('detail/<int:pk>', product_detail , name='detail'),
    path('all/', ProductList.as_view(), name='product_all'),
    path('category/', NavBar.as_view(), name='navbar'),
    path('search/', searchview, name='search'),

]
