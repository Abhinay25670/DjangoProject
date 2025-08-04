from django.contrib import admin
from .models import Medicine

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_number', 'manufacturer', 'quantity', 'expiry_date', 'user', 'is_expired', 'is_low_stock')
    list_filter = ('manufacturer', 'expiry_date', 'user')
    search_fields = ('name', 'batch_number', 'manufacturer')
    list_per_page = 25
    date_hierarchy = 'expiry_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'batch_number', 'manufacturer', 'description')
        }),
        ('Dates', {
            'fields': ('manufacturing_date', 'expiry_date')
        }),
        ('Stock Information', {
            'fields': ('quantity', 'price_per_unit', 'low_stock_threshold')
        }),
        ('User Information', {
            'fields': ('user',)
        }),
    )
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'
