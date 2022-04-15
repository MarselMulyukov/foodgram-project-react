from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "is_active", "is_staff",)
    list_filter = ("email", "username",)


admin.site.register(User, UserAdmin)
