from product.models import Product,Category

#recent product and category
def recentproduct(request):
    recent_product = Product.objects.all().order_by('-create')[:4]
    category = Category.objects.all()
    return {'recent_product': recent_product, 'category': category}