from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from orders.models import Cart
from allauth.account.models import EmailAddress
from allauth.account.admin import EmailAddressAdmin
from orders.models import OrderInfo
from django.urls import reverse
from django.utils.html import format_html

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

class OrderInfoInline(admin.TabularInline):
    model = OrderInfo
    readonly_fields = ('clickable_field', 'gateway_id', 'user', 'price', 'status', 'tracking_code', 'post_tracking_code', 'created_at')
    can_delete = False
    extra = 0

    def clickable_field(self, obj):
        link = reverse('admin:orders_orderinfo_change', args=[obj.pk])
        return format_html(f'<a href="{link}">View Details</a>')
    clickable_field.short_description = 'Order Info'

class CustomEmailAddressAdmin(EmailAddressAdmin):
    inlines = [OrderInfoInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, CustomEmailAddressAdmin)