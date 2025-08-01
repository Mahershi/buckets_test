import importlib
import traceback
import asyncio

from src.utils.parser import search_key, json_inheritance_parser
from src.runner.runner_constants import RunnerConstants
from src.tests.BaseTest import BaseTest
from src.params import TestParams, ValidationParams
from src.testlibs import BaseTestLib
from src.constants.testenv import testEnv


class TestRunner:
    def __init__(self, test_key):
        self.test_key = test_key
        self.test = None
        if not test_key:
            raise

    def run(self):
        try:
            # if need to configure host/port/client_id/client_key
            # testEnv.configure(host="", port="")
            testEnv.set_client("b07c4d0709dc7b3cfaa3bc6a4b80cc5a", "W8nmcKwxEdc_KZqYVxhLXqU5rcb30gznN21UBUD66uE")

            test_json = search_key(self.test_key, RunnerConstants.TEST_MAPPING_DIR)
            class_path = test_json['class']
            cls: BaseTest = self.load_class(class_path)
            print(f"Test Class Loaded: {cls}")

            lib_class_path = test_json['lib']
            lib_cls: BaseTestLib = self.load_class(lib_class_path)
            print(f"Test Lib Class Loaded: {lib_cls}")

            param_key = test_json['testParamsKey']
            test_params_json = search_key(param_key, RunnerConstants.TEST_PARAM_MAPPING_DIR)
            print(f"Checking {param_key} for json inheritance")
            test_params_json = json_inheritance_parser(test_params_json, RunnerConstants.TEST_PARAM_MAPPING_DIR)
            print(test_params_json)
            test_params = TestParams(test_params_json)

            validation_params = ValidationParams({})

            lib = lib_cls()
            self.test: BaseTest = cls(test_params, validation_params, lib)
            asyncio.run(self.test_runner())

        except Exception as e:
            print("Exception")
            print(traceback.format_exc())
            print(e)

    async def test_runner(self):
        self.test.setup()
        await self.test.execute()
        self.test.cleanup()

    def load_class(self, class_path: str):
        """Dynamically load a class from a string like 'src.tests.wstests.WSConnectionTest.WSConnectionTest'"""
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls: BaseTest = getattr(module, class_name)
        return cls


t = TestRunner(test_key="WSAuth100ConcurrentTest")
t.run()


