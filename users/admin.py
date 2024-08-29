from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from orders.models import Cart
from allauth.account.models import EmailAddress
from allauth.account.admin import EmailAddressAdmin

# Register your models here.

CustomUser = get_user_model()

class CartInline(admin.TabularInline):
    model = Cart
    extra = 1

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'username', 'is_staff')

class CustomEmailAddressAdmin(EmailAddressAdmin):
    inlines = [CartInline]


# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, CustomEmailAddressAdmin)