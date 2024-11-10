import json
import pytest
from django.test import Client
from django.urls import reverse

@pytest.fixture(scope="module")
def test_data():
    with open("test_data.json") as f:
        data = json.load(f)
    return data

@pytest.fixture
def client():
    return Client()
