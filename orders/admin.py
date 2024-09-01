from django.contrib import admin
from .models import OrderInfo

# Register your models here.

class OrderInfoAdmin(admin.ModelAdmin):
    model = OrderInfo
    list_display = ('gateway_id', 'user', 'price', 'tracking_code', 'post_tracking_code')

admin.site.register(OrderInfo, OrderInfoAdmin)