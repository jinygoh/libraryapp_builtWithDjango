# This file is used to configure the `library` application.
# It is related to the `settings.py` file in the `silent_library` directory, as the `INSTALLED_APPS` setting in that file will include a reference to this class.

from django.apps import AppConfig


class LibraryConfig(AppConfig):
    # This class defines the configuration for the `library` application.
    default_auto_field = "django.db.models.BigAutoField" # The default auto field to use for models in this application.
    name = "library" # The name of the application.
