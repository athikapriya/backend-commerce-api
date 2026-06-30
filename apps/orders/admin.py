from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# =============== Start OrderAdmin section ===============
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "user",
        "status",
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_id",
        "user__Username",
        'user__email',
    )

    readonly_fields = (
        "order_id",
        "created_at",
        "updated_at",
    )

    inlines =[
        OrderItemInline
    ]

admin.site.register(Order, OrderAdmin)
# =============== End OrderAdmin seciton ===============



