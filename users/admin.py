from django.contrib import admin
# 삭제하기 위해서 Group을 import
from django.contrib.auth.models import Group

# UserAdmin을 새로 커스터마이징
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
from .forms import AdminUserAddForm, AdminUserChangeForm





class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AdminUserChangeForm
    add_form = AdminUserAddForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('nickname', 'email', 'last_login', 'is_kakao','kakao_id', 'is_owner')
    list_filter = ('is_superuser', 'is_owner')
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'password',)}),
        ('Personal info(kakao)', {'fields': ('kakao_id','gender','age_range','birthday',)}),
        ('Permissions', {'fields': ('is_owner', 'is_superuser', 'is_kakao', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_owner', 'nickname'),
        }),
    )
    search_fields = ('nickname', 'is_superuser', 'is_owner', 'is_active', 'gender', 'age_range', 'birthday',)
    ordering = ('nickname',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)