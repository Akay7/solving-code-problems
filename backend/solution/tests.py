from django.urls import reverse
import pytest
from .models import Solution


@pytest.fixture(autouse=True)
def use_db(db):
    pass


@pytest.fixture
def solution_valid_payload():
    return {"code": "mock"}


def test_can_create_solution(client, solution_valid_payload):
    solution_qty = Solution.objects.count()

    response = client.post(reverse("solution-list"), solution_valid_payload)
    assert response.status_code == 201
    assert Solution.objects.count() == solution_qty + 1
