from django.contrib import admin

# Register your models here.


from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, Profile
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 2



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', )
    
    inlines = (ProfileInline,)


admin.site.register(Profile)