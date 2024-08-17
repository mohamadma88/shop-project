from django.db import models
from account.models import User


# Category model for products
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    title = models.CharField(max_length=100)
    img = models.ImageField(blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


# size model for product
class Size(models.Model):
    title = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.title


# color model for product
class Color(models.Model):
    title = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.title


# product model
class Product(models.Model):
    title = models.CharField(max_length=200)
    preview_txt = models.CharField(max_length=300, null=True, blank=True)
    img1 = models.ImageField()
    img2 = models.ImageField(null=True,blank=True)
    img3 = models.ImageField(null=True,blank=True)
    img4 = models.ImageField(null=True,blank=True)
    price = models.IntegerField(null=True, blank=True)
    discount = models.SmallIntegerField()
    size = models.ManyToManyField(Size, related_name='product')
    color = models.ManyToManyField(Color, related_name='product')
    category = models.ManyToManyField(Category)
    description = models.TextField(max_length=500)
    information = models.TextField(blank=True, null=True)
    create = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Product reviews
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    text = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# banner of index
class Banner(models.Model):
    img1 = models.ImageField(null=True,blank=True)
    img2 = models.ImageField(null=True,blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title
