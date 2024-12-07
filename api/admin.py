from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VirtualPhoneNumber, CallLog


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.

    Extends the default UserAdmin to include additional fields
    and customize the admin interface for user management.

    Key Customizations:
    - Added contact_number to list display and form fields
    - Customized list views and search capabilities
    - Enhanced permission and personal info sections
    """

    # Specify the model to be configured
    model = User

    # Columns displayed in the user list view
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "contact_number",
    ]

    # Filters available in the user list view
    list_filter = ["is_staff", "is_active"]

    # Fields that can be searched in the admin interface
    search_fields = ["username", "email"]

    # Default ordering of users
    ordering = ["username"]

    # Fieldsets define the layout of the user edit form
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

    # Fields shown when creating a new user
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

    # Enable horizontal filtering for groups and permissions
    filter_horizontal = ("groups", "user_permissions")


class VirtualPhoneNumberAdmin(admin.ModelAdmin):
    """
    Admin configuration for Virtual Phone Number model.

    Provides a customized admin interface for managing
    virtual phone numbers with enhanced visibility and search capabilities.

    Key Features:
    - Displays key information about virtual phone numbers
    - Enables searching by phone number and username
    - Allows filtering by active status
    """

    # Columns displayed in the virtual phone number list view
    list_display = ["phone_number", "user", "is_active"]

    # Fields that can be searched
    search_fields = ["phone_number", "user__username"]

    # Filters available in the list view
    list_filter = ["is_active"]


class CallLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for Call Log model.

    Provides a comprehensive admin interface for reviewing
    call logs with multiple search and filter options.

    Key Features:
    - Displays detailed call log information
    - Enables searching by virtual phone number, caller, and called numbers
    - Allows filtering by call direction and timestamp
    """

    # Columns displayed in the call log list view
    list_display = [
        "virtual_phone_number",
        "timestamp",
        "direction",
        "duration",
        "caller_number",
        "called_number",
    ]

    # Fields that can be searched
    search_fields = [
        "virtual_phone_number__phone_number",
        "caller_number",
        "called_number",
    ]

    # Filters available in the list view
    list_filter = ["direction", "timestamp"]


# Register the admin configurations
admin.site.register(User, CustomUserAdmin)
admin.site.register(VirtualPhoneNumber, VirtualPhoneNumberAdmin)
admin.site.register(CallLog, CallLogAdmin)
