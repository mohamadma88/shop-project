from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView
from product.models import Product, Category, ProductReview

# Detail product page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text')
        name = request.POST.get('name')
        email = request.POST.get('email')
        ProductReview.objects.create(text=text, name=name, email=email, user=request.user, product=product)

    return render(request, 'product/detail.html', {'product': product})

# navbar-category
class NavBar(TemplateView):
    template_name = 'include/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavBar, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

# product list
class ProductList(ListView):
    template_name = 'product/product_list.html'
    queryset = Product.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        request = self.request
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.all()
        print(colors, sizes,min_price, max_price)

        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()
        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        if min_price and max_price:
            queryset = queryset.filter(price__lte=max_price,price__gte=min_price)

        context = super(ProductList, self).get_context_data()
        context['object_list'] = queryset
        return context

# search bar
def searchview(request):
    search = request.GET.get('search')
    product_list = Product.objects.filter(title__icontains=search)
    return render(request, 'product/product_list.html', {'product_list': product_list})

