from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import Extended


class ExtendedInline(admin.StackedInline):
    """Extedned user model inline for the User admin"""
    model = Extended
    can_delete = False
    verbose_name_plural = 'extended'


class UserAdmin(BaseUserAdmin):
    """User admin class for adding custom fields like filters and inlines"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    inlines = (ExtendedInline,)


# Overrides default User Admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
