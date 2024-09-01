from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import OrderInfo, OrderedProductsInfo

# Register your models here.

class OrderedProductsInfoInline(admin.TabularInline):
    model = OrderedProductsInfo
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('order', 'product', 'quantity',)
        return self.readonly_fields

class OrderInfoAdmin(admin.ModelAdmin):
    model = OrderInfo
    list_display = ('gateway_id', 'user', 'price', 'tracking_code', 'post_tracking_code')
    inlines = [
        OrderedProductsInfoInline
    ]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + self.list_display[:4]
        return self.readonly_fields
    

    
admin.site.register(OrderInfo, OrderInfoAdmin)