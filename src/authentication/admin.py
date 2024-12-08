from django.contrib import admin
from authentication.forms import (
    UserAddForm,
    UserUpdateForm,
)
from authentication.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as SuperUserAdmin


@admin.register(User)
class UserAdmin(SuperUserAdmin):
    add_form = UserAddForm
    form = UserUpdateForm
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (
            _("Permissions"),
            {
                "fields": (
                   "is_active", "is_staff", "is_superuser", "groups", "user_permissions",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ["__str__", "is_active"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["email"]
    ordering = ["-created_at", "updated_at"]
    date_hierarchy = "created_at"