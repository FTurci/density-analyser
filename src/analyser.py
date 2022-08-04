import ovito
import numpy as np
import argparse


class Reader:
    """Complete this generic reader in the furute!!!"""
    def __init__(self, description):
        pass


        parser = argparse.ArgumentParser(description)
        parser.add_argument("path",type=str)
        parser.add_argument("--start", default=0,type=int)
        parser.add_argument("--end", default=-10,type=int)
        parser.add_argument("--stride", default=1,type=int)
        self.args = parser.parse_args()

        self.pipe = ovito.io.import_file(self.args.path, multiple_frames=True)

        self.parser = parser
        nframes = self.pipe.source.num_frames
        if self.args.end==-10:
            self.args.end = nframes




class Quadrant(Reader):
    def compute():
        start = self.args.start
        end = self.args.end
        stride = self.args.stride

        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            # only get x-y
            pos = data.particles.positions.array[:,:2]
            N = pos.shape[0]
            # count in each quadrant the number of particles
            quadrant_num = []
            for i in [-1,1]:
                for j in [-1, 1]:
                    num  = sum((i*pos[:,0]>0)*(j*pos[:,1]>0))
                    quadrant_num.append(num)
            # print(quadrant_num)
            quadrant_num = np.array(quadrant_num)
            quadrant_frac = quadrant_num/N
            print("::",frame, quadrant_frac.ptp())
