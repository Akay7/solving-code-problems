import random
import time
from typing import Tuple


def post_submission(reply: str) -> Tuple[int, str]:
    id = int(time.time() * 1000)
    status = random.choice([*["evaluation"] * 10, "correct", "wrong"])

    return id, status


def get_submission(id: int) -> Tuple[int, str]:
    status = random.choice([*["evaluation"] * 10, "correct", "wrong"])
    return id, status
