from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
	list_display = ("email", "first_name", "is_active")
	# ordering = ("-date_joined",)
	filter_horizontal = ()
	list_filter = ()
	fieldset = ()

admin.site.register(User, CustomUserAdmin)