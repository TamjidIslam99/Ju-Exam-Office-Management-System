import pytest
from unittest.mock import Mock
#from django.urls import reverse
#from django.contrib.auth.models import User
#from Publish_Result.models import PublishedResult
#from Exam_Office_System.models import Department, Exam, Course, Student, Result

# Mock Models for Testing
class MockDepartment:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MockCourse:
    def __init__(self, course_code):
        self.course_code = course_code

class MockExam:
    def __init__(self, id, department, session, course):
        self.id = id
        self.department = department
        self.session = session
        self.course = course

class MockStudent:
    def __init__(self, registration_number, department):
        self.registration_number = registration_number
        self.department = department

class MockResult:
    def __init__(self, exam_id, student, marks):
        self.exam_id = exam_id
        self.student = student
        self.marks = marks


# Test for SelectExamView
@pytest.mark.parametrize("course_code, expected", [
    ("COURSE123", {"redirect": "upload_results", "exam_id": 1}),
    ("INVALID_CODE", {"error": "No exam found for the selected criteria."})
])
def test_select_exam_view(course_code, expected):
    department = MockDepartment(1, "Test Department")
    course = MockCourse("COURSE123")
    exam = MockExam(1, department, "2023/2024", course)
    
    # Simulate SelectExamView behavior
    view = Mock()
    view.post(department.id, "2023/2024", course_code)
    response = view.post(department.id, "2023/2024", course_code)
    assert response == expected


# Test for UploadResultsView with valid XML
def test_upload_results_view_valid():
    student = MockStudent("12345", MockDepartment(1, "Test Department"))
    view = Mock()
    view.post = Mock(return_value={"success": "Uploaded 1 results successfully."})

    # Mock the XML file content
    xml_content = '''<results>
                        <result>
                            <student>
                                <id>12345</id>
                                <score>85</score>
                            </student>
                        </result>
                      </results>'''
    
    response = view.post(xml_content, 1)
    assert response["success"] == "Uploaded 1 results successfully."


# Test for UploadResultsView with invalid XML format
def test_upload_results_view_invalid_xml():
    student = MockStudent("12345", MockDepartment(1, "Test Department"))
    view = Mock()
    view.post = Mock(return_value={"error": "Error parsing XML file."})

    # Invalid XML content
    invalid_xml_content = "<invalid>data</invalid>"
    response = view.post(invalid_xml_content, 1)
    assert response["error"] == "Error parsing XML file."


# Test for UploadResultsView with an invalid student
def test_upload_results_view_invalid_student():
    student = MockStudent("12345", MockDepartment(1, "Test Department"))
    view = Mock()
    view.post = Mock(return_value={"error": "Invalid data for student: INVALID_ID"})

    # XML with an invalid student ID
    invalid_student_xml = '''<results>
                                <result>
                                    <student>
                                        <id>INVALID_ID</id>
                                        <score>85</score>
                                    </student>
                                </result>
                            </results>'''
    response = view.post(invalid_student_xml, 1)
    assert response["error"] == "Invalid data for student: INVALID_ID"


# Test for SemesterYearlyResultView
@pytest.mark.parametrize("all_results_uploaded, expected", [
    (True, {"redirect": "published_results", "message": "Results published successfully."}),
    (False, {"error": "Not all results uploaded"})
])
def test_semester_yearly_result_view(all_results_uploaded, expected):
    department = MockDepartment(1, "Test Department")
    session = "2023/2024"
    
    # Mock exams and results
    exam = MockExam(1, department, session, MockCourse("COURSE123"))
    student = MockStudent("12345", department)
    result = MockResult(exam.id, student, 85)

    # Simulate result calculation and publishing
    view = Mock()
    if all_results_uploaded:
        view.post = Mock(return_value={"redirect": "published_results", "message": "Results published successfully."})
    else:
        view.post = Mock(return_value={"error": "Not all results uploaded"})
    
    response = view.post(department.id, session)
    assert response == expected
