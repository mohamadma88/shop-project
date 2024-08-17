from django.urls import path
from .views import contactview

app_name = 'contact'
urlpatterns = [
    path('contact/', contactview, name='contact')
]

