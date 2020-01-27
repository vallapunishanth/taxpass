from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'taxpass'

    def ready(self):
        pass