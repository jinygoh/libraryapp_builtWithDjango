# File: silent_library/silent_library/urls.py
# Purpose: This file defines the project-level URL configurations for the Silent Library application.
# It's the main URL dispatcher for the entire project. When a user requests a URL, Django
# starts by looking at this file to determine which app or view should handle the request.
# It typically includes URLs from individual apps (like the 'library' app) and may contain
# project-wide URL patterns, such as the Django admin site.
"""
URL configuration for silent_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # Imports the Django admin site functionality.
from django.urls import path, include # Imports `path` for defining URL patterns and `include` for including URLconfs from other apps.

# `urlpatterns` is a list of URL patterns that Django will try to match against the requested URL.
# The order of patterns matters, as Django uses the first match it finds.
urlpatterns = [
    # Defines a URL pattern for the Django admin site.
    # The path "admin_builtin/" maps to the standard Django admin interface.
    # `admin.site.urls` provides the set of URL patterns for the admin.
    # It's renamed to "admin_builtin/" to avoid potential conflicts if the 'library' app
    # were to define its own "/admin/" URLs for a custom admin interface.
    path("admin_builtin/", admin.site.urls),

    # Includes URL patterns from the 'library' app.
    # The `path("", ...)` means that any URL that hasn't matched "admin_builtin/"
    # will be passed to the 'library.urls' module for further processing.
    # The "" prefix means that URLs defined in 'library.urls' will be appended directly
    # to the root URL of the site (e.g., if 'library.urls' has 'books/', the full path is '/books/').
    path("", include("library.urls")),
]
