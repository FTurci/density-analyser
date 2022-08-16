from analyser import Reader
import numpy as np
import matplotlib.pyplot as plt

class DensityField2d(Reader):
    """Project density and coarse grain over length dL"""
    def __init__(self):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument(,"--dl",type=float, default=1.0)
        super().open_pipe()

    def compute(self, axis=2):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        ax = [0,1,2]
        ax.pop(axis)
        x = ax[0]
        y = ax[1]
        data = self.pipe.compute(start)
        self.cell = data.cell[:]
        binningx = np.arange(self.cell[x, -1],self.cell[x, -1]+self.cell[x,x]+self.args.dl, self.args.dl)
        binningy = np.arange(self.cell[y, -1],self.cell[y, -1]+self.cell[y,y]+self.args.dl, self.args.dl)

        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            pos = data.positions.array
            H, xedge, yedge = np.histogram2d(pos[x], pos[y],bins=[binningx,binningy])
