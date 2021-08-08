import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from solution_verification_provider.models import Submission


class Solution(models.Model):
    class SolutionStatusChoices(models.TextChoices):
        EVALUATION = "evaluation", _("Evaluation")
        CORRECT = "correct", _("Correct")
        WRONG = "wrong", _("Wrong")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=10,
        choices=SolutionStatusChoices.choices,
        default=SolutionStatusChoices.EVALUATION,
    )
    code = models.TextField()
    submission = models.ForeignKey(
        Submission, null=True, related_name="solutions", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.status}"
