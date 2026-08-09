from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


# =============== Start Welcome Email Task section ===============
@shared_task
def send_welcome_email(user_email, user_name):
    send_mail(
        subject="Welcome to BackendCommerce 🎉",
        message=f"""
Hello {user_name},

Welcome to BackendCommerce!

Your account has been successfully created.

You can now:

- Browse products
- Add products to your cart
- Place orders
- Track your orders
- Manage your profile

We're happy to have you with us!

Best regards,
BackendCommerce Team
""".strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
# =============== End Welcome Email Task seciton ===============


# =============== Start Password reset email task section ===============
@shared_task
def send_password_reset_email(user_email, user_name, reset_url):
    send_mail(
        subject="Reset Your BackendCommerce Password",
        message=f"""
Hello {user_name},

We received a request to reset your BackendCommerce password.

Click the link below to reset your password:

{reset_url}

This link will expire if it is no longer valid.

If you did not request a password reset, you can safely ignore this email.

Best regards,
BackendCommerce Team
""".strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
# =============== End Password reset email task seciton ===============