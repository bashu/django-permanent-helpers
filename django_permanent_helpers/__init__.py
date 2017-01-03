import django

if django.VERSION < (1, 9):
    from .admin import (
        PermanentModelAdmin,
        PermanentModelListFilter,
    )

default_app_config = '%s.apps.AppConfig' % __name__

__version__ = '0.0.1'
