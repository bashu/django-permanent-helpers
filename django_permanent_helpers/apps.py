from django.apps import AppConfig


class AppConfig(AppConfig):
    # Name of package where `apps` module is located
    name = ".".join(__name__.split(".")[:-1])

    def __init__(self, *args, **kwargs):
        self.label = self.name.replace(".", "_")
        super().__init__(*args, **kwargs)
