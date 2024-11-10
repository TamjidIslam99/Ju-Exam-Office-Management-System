# Manage_Exam_Materials/tests/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from Exam_Office_System.models import (
    MaterialInventory,
    ExamMaterials,
    MaterialDistributionLog,
    Exam,
    Department,
    Course,
)
from Manage_Exam_Materials.forms import ExamMaterialsForm, MaterialInventoryForm, MaterialDistributionLogForm
from django.utils import timezone

User = get_user_model()

@pytest.mark.django_db
class TestExamOfficeViews:
    @pytest.fixture
    def create_exam_office_user(self):
        """Creates a test user with 'Exam_Office' role."""
        user = User.objects.create_user(
            username='exam_office_user',
            email='exam_office@example.com',
            password='password123',
            role='Exam_Office'
        )
        return user


    @pytest.fixture
    def create_teacher_user(self):
        """Creates a test user with 'Teacher' role."""
        user = User.objects.create_user(
            username='teacher_user',
            email='teacher@example.com',
            password='password123',
            role='Teacher'
        )
        return user

    @pytest.fixture
    def create_department(self, create_exam_office_user):
        """Creates a test department linked to the Exam Office user."""
        return Department.objects.create(user=create_exam_office_user, name='Computer Science and Engineering')

    @pytest.fixture
    def create_course(self, create_department):
        """Creates a test course linked to the department."""
        return Course.objects.create(
            department=create_department,
            course_code='CSE 403',
            course_title='SWE & ISD'
        )

    @pytest.fixture
    def create_exam(self, create_department, create_course, create_teacher_user):
        """Creates a test exam linked to the department and course."""
        return Exam.objects.create(
            department=create_department,
            batch='2024',
            session='Fall',
            exam_date=timezone.now().date(),
            course=create_course,
            invigilator=None,
            examiner1=None,
            examiner2=None,
            examiner3=None,
            question_creator=None,
            moderator=None,
            translator=None
        )

    @pytest.fixture
    def create_material_inventory(self, create_exam_office_user):
        """Creates a test material inventory."""
        return MaterialInventory.objects.create(
            material_type='AnswerScripts',
            stock_quantity=500,
            threshold_quantity=100
        )

    @pytest.fixture
    def create_exam_material(self, create_exam, create_material_inventory):
        """Creates a test exam material."""
        return ExamMaterials.objects.create(
            exam=create_exam,
            material_type='AnswerScripts',
            quantity=200
        )

    @pytest.fixture
    def client_logged_in_exam_office(self, client, create_exam_office_user):
        """Logs in the Exam Office user."""
        client.login(username='exam_office_user', password='password123')
        return client

    @pytest.fixture
    def client_logged_in_teacher(self, client, create_teacher_user):
        """Logs in the Teacher user."""
        client.login(username='teacher_user', password='password123')
        return client

    # 1. Access Control Tests

    def test_inventory_list_access_by_exam_office(self,client, client_logged_in_exam_office, create_material_inventory):
        """Test that Exam Office user can access the inventory list."""
        url = reverse('inventory_list')
        response = client_logged_in_exam_office.get(url)
        assert response.status_code == 200  # Check if the inventory list is showed
        assert 'inventories' in response.context  # Ensure the inventory list is in the context
        assert MaterialInventory.objects.count() == 1

    def test_inventory_list_access_by_teacher(self, client_logged_in_teacher):
        """Test that Teacher user cannot access the inventory list."""
        url = reverse('inventory_list')
        response = client_logged_in_teacher.get(url)
        assert response.status_code == 302  # Redirect
        assert response.url == reverse('login')  # Redirects to login

    def test_inventory_list_access_anonymous(self, client):
        """Test that anonymous users cannot access the inventory list."""
        url = reverse('inventory_list')
        response = client.get(url)
        assert response.status_code == 302  # Redirect
        assert response.url.startswith(reverse('login'))

    # 2. Inventory Management Tests

    def test_inventory_list_content(self, client_logged_in_exam_office, create_material_inventory):
        """Test that the inventory list displays correct data."""
        url = reverse('inventory_list')
        response = client_logged_in_exam_office.get(url)
        assert response.status_code == 200
        assert MaterialInventory.objects.count() == 1
        inventory = MaterialInventory.objects.first()
        assert inventory.material_type == 'AnswerScripts'
        assert inventory.stock_quantity == 500
        assert inventory.threshold_quantity == 100

    def test_add_inventory(self, client_logged_in_exam_office):
        """Test adding a new inventory item."""
        url = reverse('add_inventory')
        data = {
            'material_type': 'LooseSheets',
            'stock_quantity': 300,
            'threshold_quantity': 50
        }
        response = client_logged_in_exam_office.post(url, data)
        assert response.status_code == 302  # Redirect after success
        assert MaterialInventory.objects.filter(material_type='LooseSheets').exists()

    def test_edit_inventory(self, client_logged_in_exam_office, create_material_inventory):
        """Test editing an existing inventory item."""
        url = reverse('edit_inventory', args=[create_material_inventory.pk])
        data = {
            'material_type': 'AnswerScripts',
            'stock_quantity': 450,
            'threshold_quantity': 100
        }
        response = client_logged_in_exam_office.post(url, data)
        assert response.status_code == 302
        create_material_inventory.refresh_from_db()
        assert create_material_inventory.stock_quantity == 450


    # 3. Exam Materials Management Tests

    def test_exam_materials_list_access_by_exam_office(self, client_logged_in_exam_office, create_exam_material):
        """Test that Exam Office user can access the exam materials list."""
        url = reverse('exam_materials_list')
        response = client_logged_in_exam_office.get(url)
        assert response.status_code == 200
        assert 'materials' in response.context
        assert ExamMaterials.objects.count() == 1

    def test_add_exam_material(self, client_logged_in_exam_office, create_exam):
        """Test adding a new exam material."""
        url = reverse('add_exam_material')
        data = {
            'exam': create_exam.pk,
            'material_type': 'LooseSheets',
            'quantity': 150
        }
        response = client_logged_in_exam_office.post(url, data)
        assert response.status_code == 302
        assert ExamMaterials.objects.filter(material_type='LooseSheets').exists()

    def test_edit_exam_material(self, client_logged_in_exam_office, create_exam_material):
        """Test editing an existing exam material."""
        url = reverse('edit_exam_material', args=[create_exam_material.pk])
        data = {
            'exam': create_exam_material.exam.pk,
            'material_type': 'AnswerScripts',
            'quantity': 250
        }
        response = client_logged_in_exam_office.post(url, data)
        assert response.status_code == 302
        create_exam_material.refresh_from_db()
        assert create_exam_material.quantity == 250

    def test_delete_exam_material(self, client_logged_in_exam_office, create_exam_material):
        """Test deleting an exam material."""
        url = reverse('delete_exam_material', args=[create_exam_material.pk])
        response = client_logged_in_exam_office.post(url)
        assert response.status_code == 302
        assert not ExamMaterials.objects.filter(pk=create_exam_material.pk).exists()


    # 4. Material Distribution Tests

    def test_distribute_material_success(self, client_logged_in_exam_office, create_material_inventory, create_exam):
        """Test successful material distribution."""
        url = reverse('distribute_material')
        data = {
            'exam': create_exam.pk,
            'material_type': 'AnswerScripts',
            'quantity_issued': 100,
            'distribution_date': '2024-12-01'
        }
        response = client_logged_in_exam_office.post(url, data)
        assert response.status_code == 302
        # Check inventory updated
        inventory = MaterialInventory.objects.get(material_type='AnswerScripts')
        assert inventory.stock_quantity == 400
        # Check distribution log created
        assert MaterialDistributionLog.objects.filter(material_type='AnswerScripts', quantity_issued=100).exists()

    def test_distribute_material_insufficient_stock(self, client_logged_in_exam_office, create_material_inventory, create_exam):
        """Test distributing materials with insufficient stock."""
        url = reverse('distribute_material')
        data = {
            'exam': create_exam.pk,
            'material_type': 'AnswerScripts',
            'quantity_issued': 600,  # More than available
            'distribution_date': '2024-12-01'
        }
        response = client_logged_in_exam_office.post(url, data)
        assert response.status_code == 302
        # Inventory should remain unchanged
        inventory = MaterialInventory.objects.get(material_type='AnswerScripts')
        assert inventory.stock_quantity == 500
        # No distribution log should be created
        assert not MaterialDistributionLog.objects.filter(material_type='AnswerScripts', quantity_issued=600).exists()


    # 5. Inventory Alerts Tests

    def test_inventory_alerts_view_with_alerts(self, client_logged_in_exam_office, create_material_inventory):
        """Test that inventory alerts are displayed when stock is below threshold."""
        # Reduce stock below threshold
        create_material_inventory.stock_quantity = 50
        create_material_inventory.save()
        url = reverse('inventory_alerts')
        response = client_logged_in_exam_office.get(url)
        assert response.status_code == 200
        assert 'alerts' in response.context
        assert response.context['alerts'].count() == 1
        alert = response.context['alerts'].first()
        assert alert.material_type == 'AnswerScripts'
        assert alert.stock_quantity == 50


  

    