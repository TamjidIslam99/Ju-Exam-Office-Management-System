# accommodation_requests/forms.py
from django import forms
from .models import AccommodationRequest, DepartmentReview

class AccommodationRequestForm(forms.ModelForm):
    """
    Form for students to submit accommodation requests.

    This form allows students to provide details about their special needs 
    and upload relevant medical documentation to support their accommodation request.

    Attributes
    ----------
    Meta : ModelForm options
        Specifies the model and fields to include in the form.
    """
    class Meta:
        model = AccommodationRequest
        fields = ['special_needs', 'medical_documents']


class DepartmentReviewForm(forms.ModelForm):
    """
    Form for the department to provide input on the accommodation request.

    This form allows the department to submit their review and input on 
    a student's accommodation request.

    Attributes
    ----------
    Meta : ModelForm options
        Specifies the model and fields to include in the form.
    """
    class Meta:
        model = DepartmentReview
        fields = ['department_input']
