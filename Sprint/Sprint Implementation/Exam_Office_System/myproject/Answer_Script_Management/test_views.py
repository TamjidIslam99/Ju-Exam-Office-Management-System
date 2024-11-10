import pytest
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

def grade_answer_script(request, answer_script_id):
    marks = request.POST.get('marks')
    remarks = request.POST.get('remarks')
    
    if marks is not None and remarks:
        return {'status': 'Graded', 'marks': marks, 'remarks': remarks}
    return {'status': 'Failed'}

def finalize_answer_script(request, answer_script_id):
    total_marks = request.POST.get('total_marks')
    
    if total_marks:
        return {'status': 'Finalized', 'total_marks': total_marks}
    return {'status': 'Failed'}

# Test functions
def test_assign_answer_script():
    mock_data = {
        'exam': MockExam(1, 'CS101'),
        'student': MockStudent(1, 'John Doe'),
        'teacher': MockTeacher(1, 'Dr. Smith')
    }
    
    request = MockRequest(post_data={
        'student_id': mock_data['student'].id,
        'examiner_id': mock_data['teacher'].id
    })
    
    response = assign_answer_script(request, exam_id=mock_data['exam'].id)
    
    assert response['status'] == 'Success'
    assert response['grading_status'] == 'Not Graded'

def test_grade_answer_script():
    mock_data = {
        'exam': MockExam(1, 'CS101'),
        'student': MockStudent(1, 'John Doe'),
        'teacher': MockTeacher(1, 'Dr. Smith')
    }
    
    request = MockRequest(post_data={
        'marks': 90,
        'remarks': 'Good work'
    })
    
    response = grade_answer_script(request, answer_script_id=1)
    
    assert response['status'] == 'Graded'
    assert response['marks'] == 90
    assert response['remarks'] == 'Good work'

def test_finalize_answer_script():
    mock_data = {
        'exam': MockExam(1, 'CS101'),
        'student': MockStudent(1, 'John Doe'),
        'teacher': MockTeacher(1, 'Dr. Smith')
    }
    
    request = MockRequest(post_data={
        'total_marks': 100
    })
    
    response = finalize_answer_script(request, answer_script_id=1)
    
    assert response['status'] == 'Finalized'
    assert response['total_marks'] == 100

@pytest.mark.parametrize("test_case", [
    {"exam_id": 1, "student_id": 1, "examiner_id": 1, "expected_grading_status": 'Not Graded'},
    {"exam_id": 2, "student_id": 2, "examiner_id": 2, "expected_grading_status": 'Graded'} 
])
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
