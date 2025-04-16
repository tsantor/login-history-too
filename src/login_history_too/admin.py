from django.contrib import admin

from .models import UserLogin


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "ip_address",
        "browser",
        "os",
        "device",
        "platform",
        "timestamp",
    ]
    date_hierarchy = "timestamp"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        css = {
            "all": ("login_history_too/3rd-party/highlightjs/default.min.css",),
        }
        js = (
            "login_history_too/3rd-party/highlightjs/highlight.min.js",
            "login_history_too/3rd-party/ace-builds/ace.js",
            "login_history_too/js/logins.js",
        )
