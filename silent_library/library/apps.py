# File: silent_library/library/apps.py
# Purpose: This file defines application-specific configurations for the 'library' app.
# Django uses AppConfig classes to manage metadata and initialization for each installed application.
# Common uses include setting the default primary key type for models within the app,
# specifying the app's name, or running setup code when the app is loaded (e.g., connecting signals).

from django.apps import AppConfig # Imports the base AppConfig class.


# Defines the configuration for the 'library' application.
class LibraryConfig(AppConfig):
    """
    Application configuration for the 'library' app.
    This class is automatically discovered by Django if placed in apps.py.
    It needs to be referenced in the project's settings.py under INSTALLED_APPS
    (e.g., 'library.apps.LibraryConfig' or simply 'library' if Django can infer).
    """
    # `default_auto_field` specifies the type of auto-created primary key fields for models in this app.
    # `BigAutoField` is a 64-bit integer, suitable for tables that might grow very large.
    # This overrides the global DEFAULT_AUTO_FIELD setting for this app if set.
    default_auto_field = "django.db.models.BigAutoField"

    # `name` is the full Python path to the application (e.g., 'library' or 'project_name.library').
    # This is how Django identifies the application.
    name = "library"

    # `verbose_name` can be used to provide a human-readable name for this application,
    # which might be used in the Django admin interface.
    # verbose_name = "Library Management" # Example

    # The `ready()` method can be overridden to perform initialization tasks when the app is loaded,
    # such as importing signals.
    # def ready(self):
    #     import library.signals # Example: import signals.py from the current app
    #     pass
