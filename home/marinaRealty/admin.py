from django.contrib import admin
from .models import Property, PropertyImage, ContactMessage
 
 
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3  # blank upload slots shown by default
    fields = ('image', 'caption', 'order')
 
 
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'listing_type', 'status', 'price',
        'location', 'is_published', 'created_at',
    )
    list_filter = ('listing_type', 'status', 'is_published')
    search_fields = ('title', 'location', 'description')
    list_editable = ('is_published', 'status')
    ordering = ('-created_at',)
    inlines = [PropertyImageInline]
 
    fieldsets = (
        ('Listing Info', {
            'fields': ('title', 'location', 'description', 'image')
        }),
        ('Pricing & Type', {
            'fields': ('price', 'listing_type', 'status')
        }),
        ('Details', {
            'fields': ('bedrooms', 'bathrooms', 'area_sqft')
        }),
        ('Visibility', {
            'fields': ('is_published',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'preferred_date', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
 