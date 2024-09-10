from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
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
    list_display = ("email", "username", "is_staff")


class OrderInfoInline(admin.TabularInline):
    model = OrderInfo
    readonly_fields = (
        "clickable_field",
        "gateway_id",
        "user",
        "price",
        "total_products",
        "status",
        "tracking_code",
        "post_tracking_code",
        "created_at",
    )
    can_delete = False
    extra = 0
    view_on_site = False
    show_change_link = True

    def clickable_field(self, obj):
        link = reverse("admin:orders_orderinfo_change", args=[obj.pk])
        return format_html(f'<a href="{link}">View Details</a>')

    clickable_field.short_description = "Order Info"

    # changing the view on site url


"""    def get_view_on_site_url(self, obj):
        return reverse('admin:orders_orderinfo_change', args=[obj.pk])"""


class CustomEmailAddressAdmin(EmailAddressAdmin):
    inlines = [OrderInfoInline]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user",)
    readonly_fields = ("user",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, CustomEmailAddressAdmin)
admin.site.register(Profile, ProfileAdmin)
