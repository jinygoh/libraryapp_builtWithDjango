# This file is the main URL configuration for the Django project.
# It is responsible for routing incoming HTTP requests to the appropriate view functions.
# This file includes the URL configurations from other apps, such as the 'library' app.
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

# Import necessary libraries
from django.contrib import admin
from django.urls import path, include # Import include

# This list defines the URL patterns for the project.
# Each pattern maps a URL to a view function or another URL configuration.
urlpatterns = [
    # This pattern maps the 'admin/' URL to the Django admin site.
    path("admin/", admin.site.urls),
    # This pattern includes the URL configurations from the 'library' app.
    # All URLs from the 'library' app will be prefixed with an empty string.
    path("", include("library.urls")), # Include library urls
]
