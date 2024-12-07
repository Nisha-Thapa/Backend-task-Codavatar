from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VirtualPhoneNumber, CallLog


# Register the User model with the custom UserAdmin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "contact_number",
    ]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["username", "email"]
    ordering = ["username"]

    # Add the fields to be shown on the user edit form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "contact_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "contact_number",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions")


# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)


# Register Virtual Phone Number Model
class VirtualPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "user", "is_active"]
    search_fields = ["phone_number", "user__username"]
    list_filter = ["is_active"]


admin.site.register(VirtualPhoneNumber, VirtualPhoneNumberAdmin)


# Register Call Log Model
class CallLogAdmin(admin.ModelAdmin):
    list_display = [
        "virtual_phone_number",
        "timestamp",
        "direction",
        "duration",
        "caller_number",
        "called_number",
    ]
    search_fields = [
        "virtual_phone_number__phone_number",
        "caller_number",
        "called_number",
    ]
    list_filter = ["direction", "timestamp"]


admin.site.register(CallLog, CallLogAdmin)
