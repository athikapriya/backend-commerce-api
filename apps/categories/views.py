from rest_framework import generics
from django.db.models import Count

from .models import Category
from .serializers import CategorySerializer



# =============== Start Category API views section ===============
class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(
        parent__isnull=True
        ).annotate(
            total_products=Count("children__products")
            ).prefetch_related("children")
    
    serializer_class = CategorySerializer
# =============== End Category API views seciton ===============