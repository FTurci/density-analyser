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
        self.parser.add_argument("--coordcutoff",type=float, default=2.0)
        self.parser.add_argument("--clustcutoff",type=float, default=1.2)
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

        accumulate = {'sizes':[],'radii':[]}
        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            clusters = data.tables['clusters']
            sizes = clusters['Cluster Size'].array
            # ignore largest and smallest clusters
            valid = (sizes>2)*(sizes<sizes[0])

            radii = clusters['Radius of Gyration'].array[valid]
            coms = clusters['Center of Mass'].array[valid]
            valid_sizes = sizes[valid]

            accumulate['sizes'] += list(valid_sizes)
            accumulate['radii'] += list(radii)

            # plt.hist(valid_sizes)
            # print(valid_sizes)
            # print(valid_sizes.mean())
            # print(radii.mean())
            # print(sizes)
            # plt.savefig("sizes.png")
            # input("    keystroke:")

            # print(dir(clusters))
        plt.hist(accumulate['radii'], bins=32)
        plt.savefig('radii.png')
ld = LDfluct()
ld.compute()
