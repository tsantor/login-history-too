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
            "all": (
                "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.1.0/styles/default.min.css",
            ),
        }
        js = (
            "js/ace-builds/ace.js",
            "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.1.0/highlight.min.js",
            "js/logins.js",
        )
