import analyser
import ovito
from scipy.stats import binned_statistic_dd
import numpy as np

class LDfluct(analyser.Reader):
    """Compute LD fluctuations within HD phase"""
    def __init__(self,):
        description = self.__doc__
        super().__init__(description)
        super().open_pipe()


    def compute(self, threshold,binsize,coordcutoff,clustcutoff):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        self.coordcutoff = coordcutoff
        self.clustcutoff = clustcutoff


        self.pipe.modifiers.append(
            ovito.modifiers.CoordinationAnalysisModifier(
            coordcutoff=self.coordcutoff
            )
        )

        self.pipe.modifiers.append(
            ovito.modifiers.DeleteSelectedModifier()
        )

        self.pipe.modifiers.append(
            ovito.modifiers.ClusterAnalysisModifier(
            cutoff=clustcutoff,
            sort_by_size=True,
            compute_com=True,
            compute_gyration=True)
        )
        heights = []
        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            clusters = cata.tables['clusters']
            print(clusters)
