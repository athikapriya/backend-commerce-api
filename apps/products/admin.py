from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id", "name", "category", 'price', "stock", "is_active",
    )

    list_filter = (
        "category", "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        'slug': ("name",)
    }

admin.site.register(Product, ProductAdmin)