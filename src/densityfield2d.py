from analyser import Reader
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import tqdm
matplotlib.use('Agg')

class DensityField2d(Reader):
    """Project density and coarse grain over length dL"""
    def __init__(self):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument("folder",type=str)
        self.parser.add_argument("--dl",type=float, default=1.0)
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
        ox,Lx = self.cell[x,-1],self.cell[x,x]
        oy,Ly = self.cell[y,-1],self.cell[y,y]
        binningx = np.arange(ox,ox+Lx+self.args.dl, self.args.dl)
        binningy = np.arange(oy,oy+Ly+self.args.dl, self.args.dl)

        for frame in tqdm.tqdm(range(start, end, stride)):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array
            H, xedge, yedge = np.histogram2d(pos[x], pos[y],bins=[binningx,binningy])


            plt.imshow(H, origin='lower', extent = [ox,ox+Lx,oy,oy+Ly])
            print([ox,ox+Lx,oy,oy+Ly])
            plt.axis('equal')
            plt.savefig(self.args.folder+"/frame%06d.png"%frame)
            plt.colorbar()
            plt.clf()

D = DensityField2d()
D.compute()
