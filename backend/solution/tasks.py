from solving_code_problems.celery import app
from solution.models import Solution
from solution_verification_provider.provider import (
    get_or_create_submission_result,
    check_submission_result,
)
from solution_verification_provider.models import Submission


class SubmissionNotYetEvaluatedException(Exception):
    """Required just for rerun celery task."""


def update_solution_with_submission(solution: Solution, submission: Submission):
    solution.submission = submission
    solution.status = submission.status
    solution.save()
    return solution


@app.task(bind=True)
def make_submission(self, solution_id):
    solution = Solution.objects.get(id=solution_id)
    if solution.submission is None:
        submission = get_or_create_submission_result(solution.code)
        solution = update_solution_with_submission(solution, submission)
    if solution.status == Solution.SolutionStatusChoices.EVALUATION:
        check_submission.apply_async((solution.id,))


@app.task(
    bind=True,
    autoretry_for=(SubmissionNotYetEvaluatedException,),
    max_retries=None,  # never stop
    retry_backoff=3,
    retry_backoff_max=60,
)
def check_submission(self, solution_id):
    solution = Solution.objects.get(id=solution_id)
    submission = check_submission_result(solution.submission)
    solution = update_solution_with_submission(solution, submission)

    if solution.status == Solution.SolutionStatusChoices.EVALUATION:
        raise SubmissionNotYetEvaluatedException
