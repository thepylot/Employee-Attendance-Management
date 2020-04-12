from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

class AnnualLimitAdmin(admin.StackedInline):
    model = models.AnnualLimit
    extra = 1
    max_num = 1

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')} ),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields':('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    inlines = [AnnualLimitAdmin]

    class Meta:
       model = models.User


class AnnualLimitAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Leave)
admin.site.register(models.AnnualLimit, AnnualLimitAdmin)
admin.site.register(models.ProfilePic)