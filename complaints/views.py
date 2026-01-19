from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Complaint, Category, AdminResponse
from .forms import ComplaintSubmissionForm
from ml_module.classifier import predict_category


@login_required
def submit_complaint(request):
    """View for submitting a new complaint with AI classification"""
    if request.method == 'POST':
        form = ComplaintSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            
            # AI Classification: Predict category from description
            description = complaint.description
            predicted_category_name, confidence = predict_category(description)
            
            # Get or create the category object
            try:
                category_obj = Category.objects.get(name=predicted_category_name)
                complaint.predicted_category = category_obj
                complaint.final_category = category_obj  # Set as final by default
                
                messages.success(
                    request,
                    f'Complaint submitted successfully! Auto-classified as: {predicted_category_name} '
                    f'(Confidence: {confidence:.0%})'
                )
            except Category.DoesNotExist:
                messages.warning(
                    request,
                    'Complaint submitted, but category could not be auto-detected. Admin will classify it.'
                )
            
            complaint.save()
            return redirect('complaints:my_complaints')
    else:
        form = ComplaintSubmissionForm()
    
    return render(request, 'complaints/submit_complaint.html', {'form': form})


@login_required
def my_complaints(request):
    """View for user to see their own complaints"""
    complaints = Complaint.objects.filter(user=request.user).select_related(
        'predicted_category', 'final_category'
    ).prefetch_related('responses')
    
    # Pagination
    paginator = Paginator(complaints, 10)  # 10 complaints per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'complaints': page_obj,
        'total_complaints': complaints.count(),
    }
    return render(request, 'complaints/my_complaints.html', context)


@login_required
def complaint_detail(request, complaint_id):
    """View for detailed complaint information"""
    complaint = get_object_or_404(
        Complaint.objects.select_related('user', 'predicted_category', 'final_category')
        .prefetch_related('responses__admin'),
        id=complaint_id
    )
    
    # Check if user owns this complaint or is admin
    if complaint.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('complaints:my_complaints')
    
    context = {
        'complaint': complaint,
        'responses': complaint.responses.all().order_by('created_at')
    }
    return render(request, 'complaints/complaint_detail.html', context)
