from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    name = 'apps.categories'

    def ready(self):
        from . import signals