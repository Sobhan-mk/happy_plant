from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as userA
from .forms import UserChangeForm, UserCreateForm
from .models import User, Profile
from django.contrib.auth.models import Group


#در ادمین پنل برای هر کاربر ادمین اطلاعات و فرم های زیر نمایش داده می شود.
class UserAdmin(userA):
    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('username', 'email')
    list_filter = ('username', 'is_active')

    fieldsets = (
        ('user', {'fields': ('username', 'email')}),
        ('Personal info', {'fields': ('is_admin', )}),
        ('Permissions', {'fields': ('is_active', )}),
    )

    add_fieldsets = (
        (None, {'fields' : ('username', 'email', 'pass_1', 'pass_2')})
    )

    search_fields = ('username', )

    ordering = ('username', )

    filter_horizontal = ()
#register adds an object to admin panel and unregister deletes object from admin panel
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)


