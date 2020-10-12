from janis_core import JanisTransformation, JanisTransformationGraph

from janis_bioinformatics.data_types import (
    CompressedVcf,
    VcfTabix,
    Vcf,
    Bam,
    BamBai,
    VcfIdx,
)

from janis_bioinformatics.tools.samtools import SamToolsIndex_1_9
from janis_bioinformatics.tools.htslib import Tabix_1_9, BGZip_1_9
from janis_bioinformatics.tools.igvtools import IgvIndexFeature_2_5_3

transformations = [
    JanisTransformation(Bam, BamBai, SamToolsIndex_1_9(), relevant_tool_input="bam"),
    JanisTransformation(Vcf, VcfIdx, IgvIndexFeature_2_5_3()),
    JanisTransformation(Vcf, CompressedVcf, BGZip_1_9()),
    JanisTransformation(CompressedVcf, VcfTabix, Tabix_1_9()),
]


# graph = JanisTransformationGraph()
# graph.add_edges(transformations)
#
# wf = graph.build_workflow_to_translate(Vcf, VcfIdx)
#
# wf.translate("wdl")
#
# # wf.get_dot_plot(show=True)