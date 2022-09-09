from django.contrib import admin
from .models import CustomUser,Blog
from django.contrib.auth.admin import UserAdmin


# It changes the default configuration set up of admin site for Users
class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username', 'first_name','last_name')
    list_filter = ('email', 'username', 'first_name','last_name',)
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'first_name','last_name',
                    'is_active', 'is_staff','gender',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name','last_name','gender','image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        ('Personal', {'fields': ('birth_date', 'about', 'age','country')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email','gender','country','image', 'username', 'first_name','last_name', 'password1', 'password2', 'is_active', 'is_staff', 'about', 'age',
                'birth_date')}
         ),
    )


# It changes the default configuration set up of admin site for Blogs
class BlogAdminConfig(admin.ModelAdmin):
    search_fields = ('name', 'blogtype',)
    ordering = ('date_created',)
    list_display = ('name', 'tagline','blogtype',)


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Blog,BlogAdminConfig)
