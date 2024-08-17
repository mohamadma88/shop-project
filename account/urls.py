from django.urls import path
from .views import   OtpLoginView , CheckOtp , AddAddress,LoginUser
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', OtpLoginView.as_view(), name='register'),
    path('check/', CheckOtp.as_view(), name='check'),
    path('address/', AddAddress.as_view(), name='add_address'),
    path('address/', AddAddress.as_view(), name='add_address'),
]