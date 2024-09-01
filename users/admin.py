from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from orders.models import Cart
from allauth.account.models import EmailAddress
from allauth.account.admin import EmailAddressAdmin
from .models import CustomUser, UserProfile

# Register your models here.

# CustomUser = get_user_model()

class CartInline(admin.TabularInline):
    model = Cart
    extra = 1

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'username', 'is_staff')


class CustomEmailAddressAdmin(EmailAddressAdmin):
    inlines = [UserProfileInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, CustomEmailAddressAdmin)
admin.site.register(UserProfile)