import os
import operator
from pathlib import Path
from typing import Dict, Optional, List, Any

from janis_core import TOutput, File
from janis_bioinformatics.tools.bioinformaticstoolbase import (
    BioinformaticsPythonTool,
)
from janis_core import ToolMetadata, Logger, PythonTool
from janis_core.tool.tool import TTestCompared, TTestExpectedOutput, TTestCase


class InsertLineBase(BioinformaticsPythonTool):
    @staticmethod
    def code_block(
        in_file: File, line_to_insert: str, insert_after_line: int
    ) -> Dict[str, Any]:
        from shutil import copyfile

        # dst = copyfile(in_file, "./out.file")
        dst = "./output.txt"

        with open(in_file, "r") as fin, open(dst, "w") as fout:
            count = 0
            for line in fin:
                count += 1
                fout.write(line)

                if count == insert_after_line:
                    fout.write(line_to_insert + "\n")

        line_count = count + 1

        return {"out_file": dst, "line_count": line_count}

    def friendly_name(self) -> Optional[str]:
        return "Insert line to a text file"

    def outputs(self) -> List[TOutput]:
        return [TOutput("out_file", File), TOutput("line_count", int)]

    def id(self) -> str:
        return "InsertLine"

    def version(self):
        return "v0.1.0"

    def bind_metadata(self):
        return ToolMetadata(
            contributors=["Michael Franklin"],
            dateCreated="2020-07-30",
            institution="Melbourne Bioinformatics",
        )

    def tests(self):
        return [
            TTestCase(
                name="InsertLineBasic",
                input={
                    "in-file": os.path.join(self.test_data_path(), "input.txt"),
                    "line-to-insert": "abc",
                    "insert-after-line": "1"
                },
                output=[
                    TTestExpectedOutput(
                        tag="line_count",
                        compared=TTestCompared.Value,
                        operator=operator.eq,
                        expected_value=2
                    ),
                    TTestExpectedOutput(
                        tag="out_file",
                        compared=TTestCompared.FileMd5,
                        operator=operator.eq,
                        expected_value="85d7c20f3e0c7af4510ca5d1f4997b9f"
                    ),
                    TTestExpectedOutput(
                        tag="out_file",
                        compared=TTestCompared.FileDiff,
                        operator=operator.eq,
                        expected_source=os.path.join(self.test_data_path(), "expected_output.txt"),
                        expected_value=[]
                    )
                ]
            )
        ]

    # TODO: delete
    @classmethod
    def tool_full_path(cls):
        return Path(__file__).absolute()


if __name__ == "__main__":
    InsertLineBase().translate("cwl")