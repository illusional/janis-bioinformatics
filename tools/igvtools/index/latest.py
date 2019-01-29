from janis.bioinformatics.tools.igvtools.igvtoolslatest import IgvToolsLatest
from janis.bioinformatics.tools.igvtools.index.base import IgvToolsIndexBase


class IgvToolsIndexLatest(IgvToolsLatest, IgvToolsIndexBase):
    pass


if __name__ == "__main__":
    print(IgvToolsIndexLatest().help())
