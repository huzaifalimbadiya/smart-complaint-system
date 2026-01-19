from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """
    Complaint categories for classification
    These are predefined categories used by the AI classifier
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Complaint(models.Model):
    """
    Main complaint model storing user submissions
    Includes both AI-predicted and admin-confirmed categories
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200, help_text="Brief description of the issue")
    description = models.TextField(help_text="Detailed explanation of the complaint")
    image = models.ImageField(upload_to='complaints/', blank=True, null=True, help_text="Optional proof image")
    area = models.CharField(max_length=200, help_text="Location/area of the complaint")
    
    # AI Classification fields
    predicted_category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='predicted_complaints',
        help_text="Category predicted by AI"
    )
    final_category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='final_complaints',
        help_text="Final category (admin can correct AI prediction)"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes for admins only")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.id} - {self.title[:50]}"

    def get_status_badge_class(self):
        """Returns Bootstrap badge class for status"""
        badge_map = {
            'pending': 'warning',
            'in_progress': 'info',
            'resolved': 'success',
            'rejected': 'danger',
        }
        return badge_map.get(self.status, 'secondary')

    def get_category(self):
        """Returns final category if set, otherwise predicted category"""
        return self.final_category or self.predicted_category

    def save(self, *args, **kwargs):
        """Override save to set final_category to predicted if not set"""
        if not self.final_category and self.predicted_category:
            self.final_category = self.predicted_category
        super().save(*args, **kwargs)


class AdminResponse(models.Model):
    """
    Admin responses to complaints (visible to users)
    Separate from admin_notes which are internal only
    """
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_responses')
    message = models.TextField(help_text="Message visible to the user")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admin Response"
        verbose_name_plural = "Admin Responses"
        ordering = ['created_at']

    def __str__(self):
        return f"Response to #{self.complaint.id} by {self.admin.username if self.admin else 'Admin'}"
