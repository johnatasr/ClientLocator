from django.apps import AppConfig
from locator.presenters.factories import LocatorFactory


class LocatorConfig(AppConfig):
    name = "locator"

    def ready(self):
        factory = LocatorFactory()
        redis_instance = factory.create_redis_instance()
        factory.create_base_by_csv(redis_instance=redis_instance)
        factory.create_base_by_json(redis_instance=redis_instance)
