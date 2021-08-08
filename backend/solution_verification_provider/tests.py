import factory
from unittest import mock

from .models import Submission
from .provider import get_or_create_submission_result


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission


def test_get_result_if_reply_was_evaluated():
    reply = "test reply"
    SubmissionFactory(
        id=1, reply=reply, status=Submission.SubmissionStatusChoice.CORRECT
    )
    submission = get_or_create_submission_result(reply=reply)
    assert submission.id == 1
    assert submission.status == Submission.SubmissionStatusChoice.CORRECT


@mock.patch("solution_verification_provider.provider.post_submission")
@mock.patch("solution_verification_provider.provider.get_submission")
def test_get_exception_and_entity_in_db_if_reply_wasnt_evaluated_yet(
    get_submission,
    post_submission,
):
    post_submission.return_value = [100, Submission.SubmissionStatusChoice.EVALUATION]
    get_submission.return_value = [100, Submission.SubmissionStatusChoice.EVALUATION]

    submissions_qty = Submission.objects.count()
    get_or_create_submission_result(reply="test_reply")
    assert Submission.objects.count() == submissions_qty + 1
    assert post_submission.call_count == 1
    assert get_submission.call_count == 0

    # second submission shouldn't create entity in DB
    get_or_create_submission_result(reply="test_reply")
    assert Submission.objects.count() == submissions_qty + 1
    assert post_submission.call_count == 1
    assert get_submission.call_count == 1


@mock.patch(
    "solution_verification_provider.provider.get_submission",
    mock.MagicMock(return_value=[100, Submission.SubmissionStatusChoice.CORRECT]),
)
def test_get_result_if_reply_was_evaluated_between_calls():
    reply = "test reply"
    submission = SubmissionFactory(
        id=100, reply=reply, status=Submission.SubmissionStatusChoice.EVALUATION
    )
    returned_submission = get_or_create_submission_result(reply=reply)
    submission.refresh_from_db()
    assert submission.id == returned_submission.id == 100
    assert (
        submission.status
        == returned_submission.status
        == Submission.SubmissionStatusChoice.CORRECT
    )
