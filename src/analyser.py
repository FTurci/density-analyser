import ovito
import numpy as np
import argparse
import

 # Note: on the cluster, you may need to set the variable DISPLAY="" for Ovito to work
os.environ["DISPLAY"] = ""

class Reader:
    """Complete this generic reader in the furute!!!"""
    def __init__(self, description):
        parser = argparse.ArgumentParser(description)
        parser.add_argument("path",type=str)
        parser.add_argument("--start", default=0,type=int)
        parser.add_argument("--end", default=-10,type=int)
        parser.add_argument("--stride", default=1,type=int)
        parser.add_argument("-v","--verbose",action='store_true')
        self.parser = parser

    def open_pipe(self):
        self.args = self.parser.parse_args()

        self.pipe = ovito.io.import_file(self.args.path, multiple_frames=True)

        nframes = self.pipe.source.num_frames
        if self.args.end==-10:
            self.args.end = nframes


    def vprint(self,*args,**kwargs):
        if self.args.verbose==True:
            print(":v:",*args,**kwargs)



class Quadrant(Reader):
    def __init__(self,description):
        super().__init__(description)
        self.parser.add_argument("-tf","--tofile",type=str, default=None)
        super().open_pipe()

    def compute(self):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        if self.args.tofile != None:
            fopen = open(self.args.tofile,"w")

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

            self.vprint(frame, quadrant_frac.ptp())
            if 'fopen' in locals(): fopen.write(f"{frame} {str(quadrant_frac)[1:-1]} {quadrant_frac.ptp()}\n")

class LateralProfile(Reader)
