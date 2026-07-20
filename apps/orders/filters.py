import django_filters
from rest_framework import filters

from .models import Order


# =============== Start OrderFilter section ===============
class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    class Meta:
        model = Order
        fields = {
            "status" : ["exact"],
            "created_at": ["exact", "gte", "lte"],
            "total_price": ["exact", "gte", "lte"],
        }
# =============== End OrderFilter seciton ===============