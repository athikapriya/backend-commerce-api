import django_filters

from .models import Product


# =============== Start ProductFilter section ===============
class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = {
            "name" : ["iexact", "icontains"],
            "is_active" : ["exact"],
        }

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)
# =============== End ProductFilter seciton ===============