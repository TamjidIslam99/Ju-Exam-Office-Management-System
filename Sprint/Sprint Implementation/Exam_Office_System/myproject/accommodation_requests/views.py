# accommodation_requests/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AccommodationRequest, DepartmentReview
from .forms import AccommodationRequestForm, DepartmentReviewForm

@login_required
def request_accommodation(request):
    """
    Handle the accommodation request submission by the student.

    If the request is a POST request, it validates and saves the accommodation
    request submitted by the student. If successful, the student is redirected
    to the status page of the request. For a GET request, it renders an empty
    accommodation request form.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object from the student.

    Returns
    -------
    HttpResponse
        The rendered accommodation request form page if GET request, or a
        redirect to the accommodation status page if POST request is successful.
    """
    if request.method == 'POST':
        form = AccommodationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            accommodation_request = form.save(commit=False)
            accommodation_request.student = request.user.student  # assuming each user has a related Student object
            accommodation_request.save()
            messages.success(request, "Your accommodation request has been submitted successfully.")
            return redirect('accommodation_requests:status', pk=accommodation_request.pk)
    else:
        form = AccommodationRequestForm()
    
    return render(request, 'accommodation_requests/request_accommodation.html', {'form': form})


@login_required
def review_accommodation(request, pk):
    """
    Allow the department to review the student's accommodation request.

    Retrieves the accommodation request by primary key (pk). If the request is a
    POST request, it validates and saves the department's review, then updates
    the accommodation request status. For a GET request, it renders the review form.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object from the department user.
    pk : int
        The primary key of the accommodation request to review.

    Returns
    -------
    HttpResponse
        The rendered review form page if GET request, or a redirect to the
        accommodation status page if POST request is successful.
    """
    accommodation_request = AccommodationRequest.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = DepartmentReviewForm(request.POST)
        if form.is_valid():
            department_review = form.save(commit=False)
            department_review.accommodation_request = accommodation_request
            department_review.save()
            # Update the request status after review
            accommodation_request.is_approved = True  # Example logic; approval would depend on the department input
            accommodation_request.save()
            messages.success(request, "Department review has been submitted.")
            return redirect('accommodation_requests:status', pk=accommodation_request.pk)
    else:
        form = DepartmentReviewForm()
    
    return render(request, 'accommodation_requests/review_accommodation.html', {'form': form, 'accommodation_request': accommodation_request})


@login_required
def accommodation_status(request, pk):
    """
    Show the current status of the student's accommodation request.

    Retrieves the accommodation request by primary key (pk) and renders its
    current status.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object from the student or department user.
    pk : int
        The primary key of the accommodation request to display.

    Returns
    -------
    HttpResponse
        The rendered accommodation status page with details of the request.
    """
    accommodation_request = AccommodationRequest.objects.get(pk=pk)
    
    return render(request, 'accommodation_requests/accommodation_status.html', {
        'accommodation_request': accommodation_request
    })
