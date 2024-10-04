from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from oneplate.models import User,Review
# Register your models here.

# 기존 필드셋에 'nickname'과 'intro' 필드 추가
UserAdmin.fieldsets += ('Custom fields', {'fields': ('nickname', 'profile_pic','intro')}),

admin.site.register(User, UserAdmin)
admin.site.register(Review)

