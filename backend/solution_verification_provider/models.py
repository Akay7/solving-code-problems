import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Submission(models.Model):
    """Saving processed results in the DB, for reduce load at the external service"""

    class SubmissionStatusChoice(models.TextChoices):
        CORRECT = "correct", _("Correct")
        WRONG = "wrong", _("Wrong")
        EVALUATION = "evaluation", _("Evaluation")

    SUBMISSION_READY_STATUSES = {
        SubmissionStatusChoice.CORRECT,
        SubmissionStatusChoice.WRONG,
    }

    id = models.PositiveBigIntegerField(primary_key=True)
    reply = models.TextField(db_index=True)
    status = models.TextField(max_length=10, choices=SubmissionStatusChoice.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.status}"
