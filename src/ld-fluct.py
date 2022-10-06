import analyser
import ovito
from scipy.stats import binned_statistic_dd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class LDfluct(analyser.Reader):
    """Compute LD fluctuations within HD phase"""
    def __init__(self,):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument("--threshold",type=int, default=40.0)
        self.parser.add_argument("--coordcutoff",type=int, default=2.0)
        self.parser.add_argument("--clustcutoff",type=int, default=1.2)
        super().open_pipe()


    def compute(self):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        coordcutoff = self.args.coordcutoff
        clustcutoff = self.args.clustcutoff


        self.pipe.modifiers.append(
            ovito.modifiers.CoordinationAnalysisModifier(
            cutoff=coordcutoff
            )
        )
        self.pipe.modifiers.append(ovito.modifiers.ExpressionSelectionModifier
            (
            expression = f"Coordination>{self.args.threshold}"
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


        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            clusters = data.tables['clusters']
            sizes = clusters['Cluster Size'].array
            # ignore largest and smallest clusters
            valid = (sizes>2)*(sizes<sizes[0])

            radius = clusters['Radius of Gyration'].array[valid]
            com = clusters['Center of Mass'].array[valid]
            valid_sizes = sizes[valid]

            plt.hist(valid_sizes)
            print(valid_sizes)
            print(sizes)
            plt.savefig("sizes.png")
            input("    keystroke:")

            # print(dir(clusters))
ld = LDfluct()
ld.compute()
