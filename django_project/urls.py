from django.contrib import admin
from django.urls import path

admin.site.enable_nav_sidebar = False

urlpatterns = [
    path("admin/", admin.site.urls),
]
