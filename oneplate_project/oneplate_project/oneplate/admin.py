from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from oneplate.models import User
# Register your models here.

UserAdmin.fieldsets += ('Custom fields', {'fields': ('nickname', 'intro')}),

admin.site.register(User, UserAdmin)