from django.contrib import admin
from .models import Category, Complaint, AdminResponse


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """Admin interface for Complaint"""
    list_display = ('id', 'title', 'user', 'get_category_display', 'status', 'created_at')
    list_filter = ('status', 'final_category', 'predicted_category', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'area')
    ordering = ('-created_at',)
    readonly_fields = ('predicted_category', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description', 'area', 'image')
        }),
        ('AI Classification', {
            'fields': ('predicted_category', 'final_category'),
            'description': 'Predicted category is set by AI. Admin can correct it in final_category.'
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_category_display(self, obj):
        """Display final or predicted category"""
        category = obj.get_category()
        return category.name if category else 'Uncategorized'
    get_category_display.short_description = 'Category'


@admin.register(AdminResponse)
class AdminResponseAdmin(admin.ModelAdmin):
    """Admin interface for AdminResponse"""
    list_display = ('complaint', 'admin', 'created_at', 'short_message')
    list_filter = ('created_at',)
    search_fields = ('complaint__title', 'message', 'admin__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def short_message(self, obj):
        """Display truncated message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'
