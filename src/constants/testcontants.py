from enum import Enum


class TestStatus(Enum):
    QUEUED = "queued"
    FAILED = "failed"
    PASSED = "passed"
    ABORTED = "aborted"
    RUNNING = "running"
    NOT_RUN = "notrun"
