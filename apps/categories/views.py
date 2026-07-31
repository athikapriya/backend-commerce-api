from rest_framework import generics
from django.db.models import Count
from drf_spectacular.utils import extend_schema
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Category
from .serializers import CategorySerializer



# =============== Start Category API views section ===============
@extend_schema(
    summary="List Categories",
    description=(
        "Returns all parent categories with their child categories "
        "and the total number of products in each parent category."
    ),
    tags=["Categories"],
)
class CategoryAPIView(generics.ListAPIView):
    throttle_scope = "categories"
    queryset = Category.objects.filter(
        parent__isnull=True
        ).annotate(
            total_products=Count("children__products")
            ).prefetch_related("children")
    
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 60, key_prefix="category_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
# =============== End Category API views seciton ===============