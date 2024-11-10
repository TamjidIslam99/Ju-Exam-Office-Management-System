from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ExamMaterials, MaterialInventory, MaterialDistributionLog, User
from .forms import ExamMaterialsForm, MaterialInventoryForm, MaterialDistributionLogForm
from django.db.models import F
from django.core.mail import send_mail
from django.conf import settings

# Implementing necessary logic to pass the test cases in test_views.py

# 1. Custom decorator to check for Exam Office role
def exam_office_required(view_func):
    """
    Custom decorator to restrict access to users with the 'Exam Office' role.

    :param view_func: The view function being wrapped.
    :return: The wrapped view function.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated
        if request.user.role != 'Exam_Office':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('login')  # Redirect to login if user is unauthorized
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# 2.1 Inventory Management
@exam_office_required
def inventory_list(request):
    """
    Displays the list of all material inventories.

    :param request: HTTP request object.
    :return: Rendered HTML response with the list of inventories.
    """
    inventories = MaterialInventory.objects.all()
    return render(request, 'exam_management/inventory_list.html', {'inventories': inventories})


@exam_office_required
def manage_inventory(request, pk=None):
    """
    Handles the addition or editing of inventory items.

    :param request: HTTP request object.
    :param pk: Primary key of the inventory item to be edited (optional).
    :return: Rendered HTML response with the inventory form.
    """
    inventory = get_object_or_404(MaterialInventory, pk=pk) if pk else None

    if request.method == 'POST':
        form = MaterialInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory saved successfully.')
            return redirect('inventory_list')
    else:
        form = MaterialInventoryForm(instance=inventory)

    context = {
        'form': form,
        'pk': pk,
        'title': 'Edit Inventory' if pk else 'Add Inventory'
    }
    return render(request, 'exam_management/manage_inventory.html', context)


# 2.2 Exam Materials Management
@exam_office_required
def exam_materials_list(request):
    """
    Displays the list of exam materials linked to various exams.

    :param request: HTTP request object.
    :return: Rendered HTML response with the list of exam materials.
    """
    materials = ExamMaterials.objects.select_related('exam').all()
    return render(request, 'exam_management/exam_materials_list.html', {'materials': materials})


@exam_office_required
def add_exam_material(request):
    """
    Handles the addition of new exam materials.

    :param request: HTTP request object.
    :return: Rendered HTML response with the add material form or redirects to materials list.
    """
    if request.method == 'POST':
        form = ExamMaterialsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam material added successfully.')
            return redirect('exam_materials_list')
    else:
        form = ExamMaterialsForm()
    return render(request, 'exam_management/add_edit_exam_material.html', {'form': form, 'title': 'Add Exam Material'})


@exam_office_required
def edit_exam_material(request, pk):
    """
    Handles the editing of an existing exam material.

    :param request: HTTP request object.
    :param pk: Primary key of the exam material to be edited.
    :return: Rendered HTML response with the edit material form or redirects to materials list.
    """
    material = get_object_or_404(ExamMaterials, pk=pk)
    if request.method == 'POST':
        form = ExamMaterialsForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam material updated successfully.')
            return redirect('exam_materials_list')
    else:
        form = ExamMaterialsForm(instance=material)
    return render(request, 'exam_management/add_edit_exam_material.html', {'form': form, 'title': 'Edit Exam Material'})


@exam_office_required
def delete_exam_material(request, pk):
    """
    Handles the deletion of an exam material.

    :param request: HTTP request object.
    :param pk: Primary key of the exam material to be deleted.
    :return: Redirects to materials list or renders confirmation page.
    """
    material = get_object_or_404(ExamMaterials, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Exam material deleted successfully.')
        return redirect('exam_materials_list')
    return render(request, 'exam_management/delete_exam_material.html', {'material': material})


# 2.3 Material Distribution
@exam_office_required
def distribute_material(request):
    """
    Manages the distribution of materials and updates inventory stock.

    :param request: HTTP request object.
    :return: Rendered HTML response with distribution form or redirects to logs.
    """
    if request.method == 'POST':
        form = MaterialDistributionLogForm(request.POST)
        if form.is_valid():
            distribution = form.save(commit=False)
            material_type = distribution.material_type
            quantity = distribution.quantity_issued

            try:
                inventory = MaterialInventory.objects.get(material_type=material_type)
                if inventory.stock_quantity >= quantity:
                    inventory.stock_quantity = F('stock_quantity') - quantity
                    inventory.save()
                    distribution.save()
                    messages.success(request, 'Materials distributed successfully.')

                    inventory.refresh_from_db()
                    if inventory.stock_quantity < inventory.threshold_quantity:
                        send_stock_alert(inventory)
                else:
                    messages.error(request, f"Not enough stock for {material_type}. Available: {inventory.stock_quantity}")
                    return redirect('distribute_material')
            except MaterialInventory.DoesNotExist:
                messages.error(request, f"Inventory for {material_type} does not exist.")
                return redirect('distribute_material')

            return redirect('distribution_log')
    else:
        form = MaterialDistributionLogForm()
    return render(request, 'exam_management/distribute_material.html', {'form': form})


def send_stock_alert(inventory):
    """
    Sends an email alert when inventory stock falls below threshold.

    :param inventory: MaterialInventory object whose stock is below threshold.
    """
    subject = f"Stock Alert: {inventory.material_type} Below Threshold"
    message = (
        f"The stock for {inventory.material_type} has fallen below the threshold.\n"
        f"Current Stock: {inventory.stock_quantity}"
    )
    recipient_list = list(User.objects.filter(role='Exam_Office').values_list('email', flat=True))
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@exam_office_required
def distribution_log(request):
    """
    Displays a log of material distribution activities.

    :param request: HTTP request object.
    :return: Rendered HTML response with the distribution logs.
    """
    logs = MaterialDistributionLog.objects.select_related('exam').order_by('-distribution_date')
    return render(request, 'exam_management/distribution_log.html', {'logs': logs})


# 2.4 Inventory Alerts
@exam_office_required
def inventory_alerts(request):
    """
    Displays a list of inventory items that have stock below the threshold.

    :param request: HTTP request object.
    :return: Rendered HTML response with the list of inventory alerts.
    """
    alerts = MaterialInventory.objects.filter(stock_quantity__lt=F('threshold_quantity'))
    return render(request, 'exam_management/inventory_alerts.html', {'alerts': alerts})

