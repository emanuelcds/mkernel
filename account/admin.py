from django.contrib import admin
from django.contrib.auth.models import User
from account.models import Pin, Location

# Register your models here.

admin.site.register(Pin)
admin.site.register(Location)


class MyUserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('permissions')
            self.exclude.append('groups')
            self.exclude.append('is_superuser')
        return super(MyUserAdmin, self).get_form(request, obj, **kwargs)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
