from django.contrib import admin
from .models import Size, Color, Product, Category , ProductReview , Banner


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title","price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductReview)
admin.site.register(Banner)
