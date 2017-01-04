from django.contrib import admin
from django.contrib.auth.models import User
from account.models import Location

# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.username == 'emanuel':
            self.exclude.append('user_permissions')
            self.exclude.append('groups')
            self.exclude.append('is_superuser')
        return super(MyUserAdmin, self).get_form(request, obj, **kwargs)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Location)
