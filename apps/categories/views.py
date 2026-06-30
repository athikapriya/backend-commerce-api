from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer



# =============== Start Category API views section ===============
class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True).prefetch_related("children")
    serializer_class = CategorySerializer
# =============== End Category API views seciton ===============