from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Vendor_Acct
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('fullname', 'username', 'address', 'email', 'first_phone_num', 'second_phone_num', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        # (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('date_joined', 'last_login',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )

    # add_fieldsets = (
    #     (None, {
    #         # 'classes': ('wide',),
    #         'fields': ('email', 'username', 'password'),
    #     }),
    # )

admin.site.register(User_Acct, AccountAdmin)