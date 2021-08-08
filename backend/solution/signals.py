from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Solution
from .tasks import make_submission


@receiver(post_save, sender=Solution)
def post_save_solution(sender, instance: Solution, created: bool, **kwargs):
    if created:
        make_submission.apply_async((instance.id,))
