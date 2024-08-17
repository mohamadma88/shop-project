from django.shortcuts import render
from django.views.generic import View
from product.models import Banner , Category


class HomeView(View):
    def get(self, request):
        banner = Banner.objects.all()
        category = Category.objects.all()
        return render(request, 'home/index.html',{'banner':banner,'category':category})

