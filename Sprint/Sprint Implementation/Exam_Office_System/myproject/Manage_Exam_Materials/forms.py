# exam_management/forms.py

from django import forms
from .models import ExamMaterials, MaterialInventory, MaterialDistributionLog

class ExamMaterialsForm(forms.ModelForm):
    class Meta:
        model = ExamMaterials
        fields = ['exam', 'material_type', 'quantity']

class MaterialInventoryForm(forms.ModelForm):
    class Meta:
        model = MaterialInventory
        fields = ['material_type', 'stock_quantity', 'threshold_quantity']

class MaterialDistributionLogForm(forms.ModelForm):
    class Meta:
        model = MaterialDistributionLog
        fields = ['exam', 'material_type', 'quantity_issued', 'distribution_date']
        widgets = {
            'distribution_date': forms.DateInput(attrs={'type': 'date'}),
        }
