import analyser
import ovito
from scipy.stats import binned_statistic_dd
import numpy as np
import tqdm
import matplotlib.pyplot as plt
import matplotlib
import h5py
from stringato import num_word

matplotlib.use('Agg')



class CentreOfMass(analyser.Reader):
    """Compute the motion of the centre of mass."""
    def __init__(self,):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument("--copyhere",action='store_true')
        self.parser.add_argument("--tqdm",action='store_true')
        super().open_pipe()


    def compute(self):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride

        accumulate = {'sizes':[],'radii':[]}
        coms = []
        if self.args.tqdm:
            progress = tqdm.tqdm
        else:
            progress = lambda x:x
        for frame in (range(start, end, stride)):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array
            com = pos.mean(axis=0)
            coms.append(com)

        coms = np.array(coms)
        msd = np.sum((coms-coms[0])**2, axis=1)
        h5path = self.args.path+".com.analysis.h5"
        h5f = h5py.File(h5path, 'w')
        h5f.create_dataset('coms', data=coms)
        h5f.create_dataset('radii', data=msd)
        h5f.close()

        iters = np.arange(len(msd))
        p,cov = np.polyfit(iters,msd,1,cov=True)
        # print("MSD/niterations = ",num_word("eps",self.args.path),p[0], np.sqrt(cov[0,0]))
        print(num_word("eps",self.args.path), msd.var(), msd.mean())
        np.savetxt("msd.txt",list(zip(iters,msd)))
        if self.args.copyhere:
            import os
            os.system(f"cp "+h5path+" .")

cm = CentreOfMass()
cm.compute()
