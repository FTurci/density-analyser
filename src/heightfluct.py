import analyser
import ovito
from scip.stats import binned_statistic_dd

class HeighFluctuations(analyser.Reader):
    """Compute heigh fluctuations at the barrier"""
    def __init__(self,):
        description = self.__doc__
        super().__init__(description)
        super().open_pipe()


    def compute(self, threshold,binsize,cutoff):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        if self.args.tofile != None:
            fopen = open(self.args.tofile,"w")

        self.pipe.modifers.append(
            ovito.modifers.CoordinationAnalysisModifier(
            cutoff=cutoff
            )
        )

        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)

            pos = data.particles.positions.array
            coordination = data.particles.properties['Coordination']
            local_density = coordination/(4/3.*np.pi*cutoff**3)
            valid = local_density < threshold
            yz = pos[valid,1:]
            x = pos[valid,0]
            height, edges, binnumber = binned_statistic_dd(zy,x,statistic='min')

            print(height)
            print(height.mean())
