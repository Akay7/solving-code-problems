from django.urls import reverse
from django.utils import timezone
from unittest import mock
import pytest
import factory
from .models import Solution
from solution_verification_provider.tests import SubmissionFactory
from solution_verification_provider.models import Submission


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


def test_created_solution_should_have_timestamp_and_status_evaluation_and_doesnt_have_submission(
    client, solution_valid_payload
):
    datetime_before = timezone.now()
    response = client.post(reverse("solution-list"), solution_valid_payload)
    datetime_after = timezone.now()

    solution = Solution.objects.get(id=response.data["id"])
    assert datetime_before < solution.created_at < datetime_after
    assert solution.status == Solution.SolutionStatusChoices.EVALUATION
    assert solution.submission is None


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


def test_after_create_solution_celery_task_should_be_scheduled_and_submission_assigned(
    client, solution_valid_payload, settings
):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    submission = SubmissionFactory(
        id=1,
        reply=solution_valid_payload["code"],
        status=Submission.SubmissionStatusChoice.CORRECT,
    )

    response = client.post(reverse("solution-list"), solution_valid_payload)
    assert response.status_code == 201
    solution = Solution.objects.get(id=response.data["id"])

    assert solution.submission is not None
    assert solution.submission == submission
    assert solution.submission.status == solution.status


def test_if_submission_have_evaluated_solution_celery_doesnt_create_check_status_task(
    settings,
):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    code = "some code"
    submission = SubmissionFactory(
        id=1, reply=code, status=Submission.SubmissionStatusChoice.CORRECT
    )
    solution = SolutionFactory(code=code)
    assert solution.submission is None
    solution.refresh_from_db()
    assert solution.status == solution.submission.status == submission.status


@mock.patch("solution_verification_provider.provider.post_submission")
@mock.patch("solution_verification_provider.provider.get_submission")
def test_celery_shouldnt_recheck_status_of_submission_if_its_status_evaluated(
    get_submission, post_submission, settings
):
    post_submission.return_value = [100, Submission.SubmissionStatusChoice.WRONG]
    settings.CELERY_TASK_ALWAYS_EAGER = True
    solution = SolutionFactory()
    solution.refresh_from_db()
    assert solution.status == Submission.SubmissionStatusChoice.WRONG
    assert post_submission.call_count == 1
    assert get_submission.call_count == 0


@mock.patch("solution_verification_provider.provider.post_submission")
@mock.patch("solution_verification_provider.provider.get_submission")
def test_celery_should_recheck_status_of_submission_if_its_not_evaluated(
    get_submission, post_submission, settings
):
    post_submission.return_value = [100, Submission.SubmissionStatusChoice.EVALUATION]
    get_submission.return_value = [100, Submission.SubmissionStatusChoice.WRONG]
    settings.CELERY_TASK_ALWAYS_EAGER = True
    solution = SolutionFactory()
    solution.refresh_from_db()
    assert solution.status == Submission.SubmissionStatusChoice.WRONG
    assert post_submission.call_count == 1
    assert get_submission.call_count == 1


@mock.patch("solution_verification_provider.provider.post_submission")
@mock.patch("solution_verification_provider.provider.get_submission")
def test_celery_should_recheck_status_of_submission_multiple_times_if_its_not_evaluated(
    get_submission, post_submission, settings
):
    post_submission.return_value = [100, Submission.SubmissionStatusChoice.EVALUATION]

    get_submission.side_effect = (
        [100, Submission.SubmissionStatusChoice.EVALUATION],
        [100, Submission.SubmissionStatusChoice.EVALUATION],
        [100, Submission.SubmissionStatusChoice.WRONG],
    )

    get_submission.return_value = [100, Submission.SubmissionStatusChoice.WRONG]
    settings.CELERY_TASK_ALWAYS_EAGER = True
    solution = SolutionFactory()
    solution.refresh_from_db()
    assert solution.status == Submission.SubmissionStatusChoice.WRONG
    assert post_submission.call_count == 1
    assert get_submission.call_count == 3
