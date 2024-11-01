import xml.etree.ElementTree as ET
import pytest

# Mock classes to simulate the models
class Department:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Course:
    def __init__(self, course_code):
        self.course_code = course_code


class Exam:
    def __init__(self, id, department, session, course):
        self.id = id
        self.department = department
        self.session = session
        self.course = course


class Student:
    def __init__(self, registration_number):
        self.registration_number = registration_number


class Result:
    def __init__(self, exam_id, student, marks):
        self.exam_id = exam_id
        self.student = student
        self.marks = marks


class UploadResultsView:
    def __init__(self, students):
        self.students = students
        self.results = []

    def post(self, uploaded_file, exam_id):
        try:
            tree = ET.ElementTree(ET.fromstring(uploaded_file))
            root = tree.getroot()
            for result in root.findall('result'):
                student_registration_number = result.find('student/id').text
                score = int(result.find('student/score').text)

                student = next((s for s in self.students if s.registration_number == student_registration_number), None)
                if student:
                    self.results.append(Result(exam_id, student, score))
                else:
                    return {"error": f"Invalid data for student: {student_registration_number}"}

            return {"success": f"Uploaded {len(self.results)} results successfully."}
        except ET.ParseError:
            return {"error": "Error parsing XML file."}


class SelectExamView:
    def __init__(self, exams):
        self.exams = exams

    def post(self, department_id, session, course_code):
        exams = [exam for exam in self.exams if (
            exam.department.id == department_id and
            exam.session == session and
            exam.course.course_code == course_code
        )]

        if exams:
            return {"redirect": "upload_results", "exam_id": exams[0].id}
        else:
            return {"error": "No exam found for the selected criteria."}


# Test Cases
@pytest.mark.parametrize("course_code, expected", [
    ("COURSE123", {"redirect": "upload_results", "exam_id": 1}),
    ("INVALID_CODE", {"error": "No exam found for the selected criteria."})
])
def test_select_exam_view(course_code, expected):
    department = Department(1, "Test Department")
    course = Course("COURSE123")
    exam = Exam(1, department, "2023/2024", course)
    view = SelectExamView([exam])

    response = view.post(department.id, "2023/2024", course_code)
    assert response == expected


def test_upload_results_view_valid():
    student = Student("12345")
    view = UploadResultsView([student])

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
    assert len(view.results) == 1
    assert view.results[0].marks == 85


def test_upload_results_view_invalid_xml():
    student = Student("12345")
    view = UploadResultsView([student])

    response = view.post("<invalid>data</invalid>", 1)
    assert response["error"] == "Error parsing XML file."


def test_upload_results_view_invalid_student():
    student = Student("12345")
    view = UploadResultsView([student])

    xml_content = '''<results>
                        <result>
                            <student>
                                <id>INVALID_ID</id>
                                <score>85</score>
                            </student>
                        </result>
                      </results>'''
    response = view.post(xml_content, 1)
    assert response["error"] == "Invalid data for student: INVALID_ID"
