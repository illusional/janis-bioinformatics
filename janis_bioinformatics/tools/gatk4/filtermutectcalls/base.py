from abc import ABC
from typing import Dict, Any

from janis_core import (
    ToolInput,
    ToolOutput,
    InputSelector,
    CaptureType,
    File,
    ToolMetadata,
    get_value_for_hints_and_ordered_resource_tuple,
    Filename,
)
from janis_unix.data_types import TextFile

from janis_bioinformatics.data_types import VcfIdx, FastaWithDict, Vcf, VcfTabix
from ..gatk4toolbase import Gatk4ToolBase

CORES_TUPLE = [
    # (CaptureType.key(), {
    #     CaptureType.CHROMOSOME: 2,
    #     CaptureType.EXOME: 2,
    #     CaptureType.THIRTYX: 2,
    #     CaptureType.NINETYX: 2,
    #     CaptureType.THREEHUNDREDX: 2
    # })
]

MEM_TUPLE = [
    (
        CaptureType.key(),
        {
            CaptureType.TARGETED: 32,
            CaptureType.CHROMOSOME: 64,
            CaptureType.EXOME: 64,
            CaptureType.THIRTYX: 64,
            CaptureType.NINETYX: 64,
            CaptureType.THREEHUNDREDX: 64,
        },
    )
]


class Gatk4FilterMutectCallsBase(Gatk4ToolBase, ABC):
    @classmethod
    def gatk_command(cls):
        return "FilterMutectCalls"

    def tool(self):
        return "Gatk4FilterMutectCalls"

    def friendly_name(self):
        return "GATK4: GetFilterMutectCalls"

    def inputs(self):
        return [
            *super().inputs(),
            *Gatk4FilterMutectCallsBase.additional_args,
            ToolInput("vcf", VcfTabix, prefix="-V", doc="vcf to be filtered"),
            ToolInput(
                "reference", FastaWithDict, prefix="-R", doc="Reference sequence file"
            ),
            ToolInput(
                "outputFilename", Filename(extension=".vcf.gz"), position=2, prefix="-O"
            ),
        ]

    def outputs(self):
        return [
            ToolOutput(
                "out",
                VcfTabix,
                glob=InputSelector("outputFilename"),
                doc="vcf containing filtered calls",
            )
        ]

    def cpus(self, hints: Dict[str, Any]):
        val = get_value_for_hints_and_ordered_resource_tuple(hints, CORES_TUPLE)
        if val:
            return val
        return 1

    def memory(self, hints: Dict[str, Any]):
        val = get_value_for_hints_and_ordered_resource_tuple(hints, MEM_TUPLE)
        if val:
            return val
        return 16

    additional_args = [
        ToolInput(
            "contaminationTable",
            File(optional=True),
            prefix="--contamination-table",
            doc="Tables containing contamination information.",
        ),
        ToolInput(
            "segmentationFile",
            File(optional=True),
            prefix="--tumor-segmentation",
            doc="Tables containing tumor segments' minor allele fractions for germline hets emitted by CalculateContamination",
        ),
        ToolInput(
            "statsFile",
            File(optional=True),
            prefix="--stats",
            doc="The Mutect stats file output by Mutect2",
        ),
        ToolInput(
            "readOrientationModel",
            File(optional=True),
            prefix="--orientation-bias-artifact-priors",
            doc="One or more .tar.gz files containing tables of prior artifact probabilities for the read orientation filter model, one table per tumor sample",
        ),
    ]

    def bind_metadata(self):
        from datetime import date

        return ToolMetadata(
            contributors=["Hollizeck Sebastian"],
            dateCreated=date(2019, 9, 9),
            dateUpdated=date(2019, 9, 9),
            institution="Broad Institute",
            doi=None,
            citation="TBD",
            keywords=["gatk", "gatk4", "broad", "mutect2", "FilterMutectCalls"],
            documentationUrl="https://software.broadinstitute.org/gatk/documentation/tooldocs/4.1.2.0/org_broadinstitute_hellbender_tools_walkers_mutect_Mutect2.php",
            documentation="""
Filter variants in a Mutect2 VCF callset.

FilterMutectCalls applies filters to the raw output of Mutect2. Parameters are contained in M2FiltersArgumentCollection and described in https://github.com/broadinstitute/gatk/tree/master/docs/mutect/mutect.pdf. To filter based on sequence context artifacts, specify the --orientation-bias-artifact-priors [artifact priors tar.gz file] argument one or more times. This input is generated by LearnReadOrientationModel.

If given a --contamination-table file, e.g. results from CalculateContamination, the tool will additionally filter on contamination fractions. This argument may be specified with a table for one or more tumor sample. Alternatively, provide a numerical fraction to filter with the --contamination argument. FilterMutectCalls can also be given one or more --tumor-segmentation files, which are also output by CalculateContamination.
""".strip(),
        )
