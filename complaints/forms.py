from django import forms
from .models import Complaint, AdminResponse, Category


class ComplaintSubmissionForm(forms.ModelForm):
    """Form for users to submit complaints"""
    
    class Meta:
        model = Complaint
        fields = ('title', 'description', 'area', 'image')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief summary of your complaint',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Provide detailed description of the issue...',
                'required': True
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location/Area where the issue exists',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Complaint Title',
            'description': 'Detailed Description',
            'area': 'Location/Area',
            'image': 'Upload Image (Optional)'
        }
        help_texts = {
            'image': 'Upload a photo as proof (Max 5MB, JPG/PNG)'
        }

    def clean_image(self):
        """Validate image size"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image size should not exceed 5MB')
        return image


class ComplaintUpdateForm(forms.ModelForm):
    """Form for admins to update complaint status and category"""
    
    class Meta:
        model = Complaint
        fields = ('status', 'final_category', 'admin_notes')
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'final_category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Internal notes (not visible to users)'
            }),
        }


class AdminResponseForm(forms.ModelForm):
    """Form for admins to respond to complaints"""
    
    class Meta:
        model = AdminResponse
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your response to the user...',
                'required': True
            }),
        }
        labels = {
            'message': 'Response Message'
        }


class ComplaintSearchForm(forms.Form):
    """Form for searching and filtering complaints"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, description, or area...'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Complaint.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
