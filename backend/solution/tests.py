from django.urls import reverse
from django.utils import timezone
import pytest
import factory
from .models import Solution


class SolutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solution


@pytest.fixture
def solution_valid_payload():
    return {"code": "mock"}


def test_can_create_solution(client, solution_valid_payload):
    solution_qty = Solution.objects.count()

    response = client.post(reverse("solution-list"), solution_valid_payload)
    assert response.status_code == 201
    assert Solution.objects.count() == solution_qty + 1


def test_created_solution_should_have_timestamp_and_status_evaluation(
    client, solution_valid_payload
):
    datetime_before = timezone.now()
    response = client.post(reverse("solution-list"), solution_valid_payload)
    datetime_after = timezone.now()

    solution = Solution.objects.get(id=response.data["id"])
    assert datetime_before < solution.created_at < datetime_after
    assert solution.status == Solution.SolutionStatusChoices.EVALUATION


def test_cant_create_solution_with_wrong_status(client, solution_valid_payload):
    solution_valid_payload["status"] = Solution.SolutionStatusChoices.CORRECT
    response = client.post(reverse("solution-list"), solution_valid_payload)
    assert response.status_code == 201
    solution = Solution.objects.get(id=response.data["id"])
    assert solution.status == Solution.SolutionStatusChoices.EVALUATION


def test_cant_update_solution(client, solution_valid_payload):
    code = "some code"
    solution = SolutionFactory(code=code)

    url = reverse("solution-detail", args=(solution.id,))
    response = client.put(url, solution_valid_payload, content_type="application/json")
    assert response.status_code == 405
    response = client.patch(
        url, solution_valid_payload, content_type="application/json"
    )
    assert response.status_code == 405

    solution.refresh_from_db()
    assert solution.code == code


def test_cant_delete_solution(client):
    solution = SolutionFactory()

    url = reverse("solution-detail", args=(solution.id,))
    response = client.delete(url)
    assert response.status_code == 405

    solution.refresh_from_db()  # check that object still in the DB
