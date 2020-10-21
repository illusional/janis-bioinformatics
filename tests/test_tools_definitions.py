import unittest
from parameterized import parameterized

import janis_bioinformatics
from janis_core.tool.test_definitions import ToolEvaluator
from janis_core.tool import test_helpers as test_helper

all_tools = test_helper.get_all_tools([janis_bioinformatics.tools])

all_versioned_tools = []
# TODO: revert to full list
for tool_versions in all_tools:
# for tool_versions in all_tools[148:152]:
    for versioned_tool in tool_versions:
        all_versioned_tools.append(versioned_tool)


class TestToolsDefinitions(unittest.TestCase):
    failed = {}
    succeeded = set()

    @parameterized.expand([
        [t.id(), t] for t in all_versioned_tools
    ])
    def test_all_tools(self, name, tool):
        evaluation = ToolEvaluator.evaluate(tool)

        if evaluation is True:
            self.succeeded.add(tool.versioned_id())
        else:
            self.failed[tool.versioned_id()] = evaluation
            raise Exception(evaluation)

    def test_report(self):
        test_helper.print_test_report(failed=self.failed, succeeded=self.succeeded)

        if (len(self.failed) > 0):
            raise Exception(
                f"There were {len(self.failed)} tool(s) that did not contain sufficient metadata to include in the "
                f"janis_* repository. Please check to ensure your tool is in the list below"
            )
