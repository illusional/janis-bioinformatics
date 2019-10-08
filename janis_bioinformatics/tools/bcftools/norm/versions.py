from ..bcftools_1_5 import BcfTools_1_5
from ..bcftools_1_9 import BcfTools_1_9
from .base import BcfToolsNormBase


class BcfToolsNorm_1_5(BcfTools_1_5, BcfToolsNormBase):
    pass


class BcfToolsNorm_1_9(BcfTools_1_9, BcfToolsNormBase):
    pass


BcfToolsNormLatest = BcfToolsNorm_1_9
