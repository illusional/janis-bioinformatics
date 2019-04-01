from typing import List

from janis import ToolOutput, ToolInput, File, String, Int, Filename, InputSelector
from janis.unix.data_types.tsv import Tsv

from janis_bioinformatics.data_types import Vcf

from janis_bioinformatics.tools import BioinformaticsTool


class CombineVariantsBase(BioinformaticsTool):
    @staticmethod
    def tool() -> str:
        return "combinevariants"

    def friendly_name(self) -> str:
        return "Combine Variants"

    @staticmethod
    def base_command():
        return "combine_vcf.py"

    def inputs(self) -> List[ToolInput]:
        return [
            ToolInput("outputFilename", Filename(extension=".vcf")),
            ToolInput("regions", Filename(extension=".tsv"), prefix="--regions",
                      doc="Region file containing all the variants, used as samtools mpileup"),

            ToolInput("vcfs", Vcf(), prefix="-i",
                      doc="input vcfs, the priority of the vcfs will be based on the order of the input"),
            ToolInput("columns", String(), prefix="--columns",
                      doc="Columns to keep, seperated by space output vcf (unsorted)"),

            ToolInput("normal", String(), prefix="--normal",
                      doc="Sample id of germline vcf, or normal sample id of somatic vcf"),
            ToolInput("tumor", String(), prefix="--tumor", doc="tumor sample ID, required if inputs are somatic vcfs"),
            ToolInput("priority", Int(), prefix="--priority",
                      doc="The priority of the callers, must match with the callers in the source header")
        ]

    def outputs(self) -> List[ToolOutput]:
        return [
            ToolOutput("vcf", Vcf(), InputSelector("outputFilename")),
            (ToolOutput("tsv", Tsv(), InputSelector("regions")))
        ]