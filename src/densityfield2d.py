from analyser import Reader
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import h5py
import tqdm
matplotlib.use('Agg')

class DensityField2d(Reader):
    """Project density and coarse grain over length dL"""
    def __init__(self):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument("folder",type=str)
        self.parser.add_argument("--dl",type=float, default=1.0)
        self.parser.add_argument("--hdf5",action='store_true')
        self.parser.add_argument("--average",action='store_true')
        super().open_pipe()

    def compute(self, axis=2):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        ax = [0,1,2]
        ax.pop(axis)
        x = ax[0]
        y = ax[1]
        z = axis
        data = self.pipe.compute(start)
        self.cell = data.cell[:]
        ox,Lx = self.cell[x,-1],self.cell[x,x]
        oy,Ly = self.cell[y,-1],self.cell[y,y]
        oz,Lz = self.cell[z,-1],self.cell[z,z]
        dl = self.args.dl
        binningx = np.arange(ox,ox+Lx+dl, dl)
        binningy = np.arange(oy,oy+Ly+dl, dl)

        # fg, ax = plt.subplots(figsize=(10,10))
        if self.args.hdf5==True:
            h5f = h5py.File(self.args.folder+f'/hist-data-dl{dl}.h5', 'w')
            h5f.create_dataset('Ls', data=[Lx,Ly,Lz])
            h5f.create_dataset('binning_x', data=binningx)
            h5f.create_dataset('binning_y', data=binningy)


        for frame in tqdm.tqdm(range(start, end, stride)):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array
            H, xedge, yedge = np.histogram2d(pos[:,x], pos[:,y],bins=[binningx,binningy])


            plt.imshow(H/(dl*dl*Lz), origin ='lower', extent = [ox,ox+Lx,oy,oy+Ly],
            vmin = 0 , vmax= 1.4
            )

            plt.xlim(ox,ox+Lx)
            plt.ylim(oy,oy+Ly)
            plt.tight_layout()
            # plt.axis('equal')
            plt.colorbar()
            plt.savefig(self.args.folder+"/frame%06d.png"%frame)
            plt.clf()

            # write to file if requested
            if self.args.hdf5==True:
                h5f.create_dataset('frame_%d'%frame, data=H.astype(np.ubyte))

        if self.args.hdf5==True:
            h5f.close()


D = DensityField2d()
D.compute()
