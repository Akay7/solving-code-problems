from .models import Submission
from .wrapper import post_submission, get_submission


def get_or_create_submission_result(reply: str) -> Submission:
    submissions = Submission.objects.filter(reply=reply)
    ready_submissions = submissions.filter(
        status__in=Submission.SUBMISSION_READY_STATUSES
    )
    if evaluated_submission := ready_submissions.first():
        return evaluated_submission

    if not_evaluated_submission := submissions.filter(
        status=Submission.SubmissionStatusChoice.EVALUATION
    ).first():
        id_, status = get_submission(not_evaluated_submission.id)
    else:
        id_, status = post_submission(reply)
    submission, _created = Submission.objects.update_or_create(
        id=id_, defaults=dict(reply=reply, status=status)
    )
    return submission
