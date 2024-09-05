from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import OrderInfo, OrderedProductsInfo

# Register your models here.

class OrderedProductsInfoInline(admin.TabularInline):
    model = OrderedProductsInfo
    fields = ('order', 'product', 'quantity',)
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('order', 'product', 'quantity',)
        return self.readonly_fields

class OrderInfoAdmin(admin.ModelAdmin):
    model = OrderInfo
    list_display = ('tracking_code', 'user', 'price', 'status', 'created_at', 'post_tracking_code', )
    fields = ('gateway_id', 'user', 'total_products', 'price', 'status', 'created_at', 'tracking_code', 'post_tracking_code', )
    inlines = [
        OrderedProductsInfoInline
    ]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + self.fields[:7]
        return self.readonly_fields
    

    
admin.site.register(OrderInfo, OrderInfoAdmin)