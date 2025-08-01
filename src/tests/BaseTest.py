from abc import ABC
from src.params import TestParams, ValidationParams
from src.testlibs import BaseTestLib
from src.constants import TestStatus


class BaseTest(ABC):
    status = TestStatus.NOT_RUN

    def __init__(self, testParams: TestParams, validationParams: ValidationParams, testLib: BaseTestLib):
        self.setRunning()
        self.testParams = testParams
        self.validationParams = validationParams
        self.testLib: BaseTestLib = testLib

    def setup(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError

    def setPass(self):
        print("Test Result: PASS")
        status = TestStatus.PASSED

    def setFail(self):
        print("Test Result: FAIL")
        status = TestStatus.FAILED

    def setRunning(self):
        print("Test Result: RUNNING")
        status = TestStatus.RUNNING
