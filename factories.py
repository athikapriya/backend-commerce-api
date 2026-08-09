import factory
from factory.django import DjangoModelFactory

from apps.users.models import User
from apps.categories.models import Category
from apps.products.models import Product


# =============== Start UserFactory section ===============
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "TestPassword123!")
    is_staff = False
# =============== End UserFactory seciton ===============


# =============== Start AdminFactory section ===============
class AdminFactory(UserFactory):
    is_staff = True
# =============== End AdminFactory seciton ===============


# =============== Start CategoryFactory section ===============
class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
# =============== End CategoryFactory seciton ===============


# =============== Start ProductFactory section ===============
class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("sentence")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True,)
    stock = 20
    is_active = True
# =============== End ProductFactory seciton ===============