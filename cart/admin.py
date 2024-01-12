from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, DeliveryTimeModel, OrderItemHistory
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete', 'transaction_id', 'delivery_day', 'online_method', 'offline_method', 'sent']
    list_filter = ['complete']
    ordering = ['-date_ordered']
    search_fields = ('customer',)

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'date_added']
    # list_filter = ['product']
    ordering = ['-date_added']
    search_fields = ('product', 'order')
admin.site.register(OrderItem, OrderItemAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'address', 'province', 'city', 'zipcode', 'phone', 'selected']
    list_filter = ['province', 'city']
    ordering = ['-id', '-city']
    search_fields = ('province', 'city', 'zipcode', 'phone')
admin.site.register(ShippingAddress, ShippingAddressAdmin)


class DeliveryTimeModelAdmin(admin.ModelAdmin):
    list_display = ['day', 'flags', 'time1', 'time1_flag', 'time2', 'time2_flag', 'time3', 'time3_flag', 'time4', 'time4_flag']
admin.site.register(DeliveryTimeModel, DeliveryTimeModelAdmin)


class OrderItemHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity', 'delivery_time_bound', 'address', 'addedtime', 'transaction_id']
admin.site.register(OrderItemHistory, OrderItemHistoryAdmin)
