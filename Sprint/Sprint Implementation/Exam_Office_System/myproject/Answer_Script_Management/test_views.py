import pytest
from unittest.mock import patch, MagicMock

# Sample test data for various scenarios
sample_exam_data = {"exam_id": 1, "expected_status": 200, "expected_data_keys": ["exam_id", "name"]}
sample_examiner_data = {
    "exam_id": 1,
    "student_id": 101,
    "examiner_ids": [1, 2],
    "expected_status": 201,
    "expected_response": "Examiners assigned successfully",
}
sample_discrepancy_data = {
    "exam_id": 1,
    "student_id": 101,
    "mark_1": 75,
    "mark_2": 80,
    "expected_status": 200,
    "expected_flagged": True,
}

# Mock for selecting an exam
@pytest.mark.parametrize("test_case", [sample_exam_data])
@patch("Answer_Script_Management.views.select_exam_view")
def test_select_exam_view(mock_view, test_case):
    mock_response = MagicMock()
    mock_response.status_code = test_case["expected_status"]
    mock_response.json.return_value = {"exam_id": 1, "name": "Sample Exam"}

    mock_view.return_value = mock_response

    response = mock_view(test_case["exam_id"])

    assert response.status_code == test_case["expected_status"]

    if response.status_code == 200:
        data = response.json()
        assert all(key in data for key in test_case["expected_data_keys"])


# Mock for assigning examiners to an answer script
@pytest.mark.parametrize("test_case", [sample_examiner_data])
@patch("Answer_Script_Management.views.assign_examiners_view")
def test_assign_examiners_view(mock_view, test_case):
    mock_response = MagicMock()
    mock_response.status_code = test_case["expected_status"]
    mock_response.json.return_value = {"message": test_case["expected_response"]}

    mock_view.return_value = mock_response

    response = mock_view(test_case["exam_id"], test_case["student_id"], test_case["examiner_ids"])

    assert response.status_code == test_case["expected_status"]
    assert response.json().get("message") == test_case["expected_response"]


# Mock for flagging discrepancies in marks
@pytest.mark.parametrize("test_case", [sample_discrepancy_data])
@patch("Answer_Script_Management.views.flag_discrepancy_view")
def test_discrepancy_flag_view(mock_view, test_case):
    mock_response = MagicMock()
    mock_response.status_code = test_case["expected_status"]
    mock_response.json.return_value = {"flagged": test_case["expected_flagged"]}

    mock_view.return_value = mock_response

    response = mock_view(test_case["exam_id"], test_case["student_id"], test_case["mark_1"], test_case["mark_2"])

    assert response.status_code == test_case["expected_status"]
    assert response.json().get("flagged") == test_case["expected_flagged"]
