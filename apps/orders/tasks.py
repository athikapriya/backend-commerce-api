from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


# =============== Start order confirmation email task section ===============
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_order_confirmation_email(self, user_email, user_name, order_id, total_price):
    send_mail(
        subject=f"Order #{order_id} Confirmed 🎉",
        message=f"""
Hello {user_name},

Thank you for your order!

Your order has been successfully placed.

Order ID: {order_id}
Total Amount: ${total_price}

We'll notify you when your order status changes.

Thank you for shopping with BackendCommerce!

Best regards,
BackendCommerce Team
""".strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
# =============== End order confirmation email task seciton ===============


# =============== Start order status update email section ===============
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_order_status_email(self, user_email, user_name, order_id, order_status):
    send_mail(
        subject=f"Order #{order_id} Status Update",
        message=f"""
Hello {user_name},

Your BackendCommerce order has been updated.

Order ID: {order_id}
New Status: {order_status}

We'll keep you updated about your order.

Thank you for shopping with BackendCommerce!

Best regards,
BackendCommerce Team
""".strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
# =============== End order status update email seciton ===============