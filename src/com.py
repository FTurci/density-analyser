import analyser
import ovito
from scipy.stats import binned_statistic_dd
import numpy as np
import tqdm
import matplotlib.pyplot as plt
import matplotlib
import h5py
matplotlib.use('Agg')



class CentreOfMass(analyser.Reader):
    """Compute LD fluctuations within HD phase"""
    def __init__(self,):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument("--copyhere",action='store_true')
        super().open_pipe()


    def compute(self):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride

        accumulate = {'sizes':[],'radii':[]}
        coms = []
        for frame in tqdm.tqdm(range(start, end, stride)):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array
            com = pos.mean(axis=0)
            coms.append(com)

        coms = np.array(coms)
        msd = (coms-coms[0])**2
        h5path = self.args.path+".com.analysis.h5"
        h5f = h5py.File(h5path, 'w')
        h5f.create_dataset('coms', data=coms)
        h5f.create_dataset('radii', data=msd)
        h5f.close()
        if self.args.copyhere:
            import os
            os.system(f"cp "+h5path+" .")

ld = LDfluct()
ld.compute()
