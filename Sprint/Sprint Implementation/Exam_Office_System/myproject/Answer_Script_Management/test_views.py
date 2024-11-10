import pytest
import json
from unittest.mock import MagicMock

# Mocking the models and views directly
class MockExam:
    def __init__(self, exam_id, exam_name):
        self.id = exam_id
        self.name = exam_name

class MockTeacher:
    def __init__(self, teacher_id, teacher_name):
        self.id = teacher_id
        self.name = teacher_name

class MockStudent:
    def __init__(self, student_id, student_name):
        self.id = student_id
        self.name = student_name

class MockRequest:
    def __init__(self, post_data=None):
        self.POST = post_data if post_data else {}

# Mock view functions (simulating what they do without Django)
def assign_answer_script(request, exam_id):
    student_id = request.POST.get('student_id')
    examiner_id = request.POST.get('examiner_id')
    
    # Simulate business logic based on mock data
    if student_id and examiner_id:
        return {'status': 'Success', 'exam_id': exam_id, 'grading_status': 'Not Graded'}
    return {'status': 'Failed'}

# Load test cases from the JSON file
def load_test_cases():
    with open('test_cases.json', 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("test_case", load_test_cases())
def test_parametrized_assign_answer_script(test_case):
    mock_data = {
        'exam': MockExam(test_case['exam_id'], 'CS101'),
        'student': MockStudent(test_case['student_id'], 'John Doe'),
        'teacher': MockTeacher(test_case['examiner_id'], 'Dr. Smith')
    }
    
    request = MockRequest(post_data={
        'student_id': test_case['student_id'],
        'examiner_id': test_case['examiner_id']
    })
    
    response = assign_answer_script(request, exam_id=mock_data['exam'].id)
    
    assert response['status'] == 'Success'
    assert response['grading_status'] == test_case['expected_grading_status']

