from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, VirtualPhoneNumber, CallLog

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )


# Inline for Call Logs (to display in Virtual Phone Number admin)
class CallLogInline(admin.TabularInline):
    model = CallLog
    extra = 1
    fields = ('call_type', 'timestamp', 'duration', 'details')
    readonly_fields = ('timestamp',)


# Virtual Phone Number Admin
@admin.register(VirtualPhoneNumber)
class VirtualPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('phone_number', 'user__email', 'user__name')
    ordering = ('-created_at',)
    inlines = [CallLogInline]


# Call Log Admin
@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ('virtual_phone_number', 'call_type', 'timestamp', 'duration')
    list_filter = ('call_type', 'timestamp')
    search_fields = ('virtual_phone_number__phone_number', 'details')
    ordering = ('-timestamp',)
