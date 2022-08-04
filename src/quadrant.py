import ovito
import numpy as np
import argparse


parser = argparse.ArgumentParser("Analyse the density difference in the four quadrants of the plane orthogonal to z")
parser.add_argument("path")
parser.add_argument("--start", default=0,type=int)
parser.add_argument("--end", default=-10,type=int)
parser.add_argument("--stride", default=1,type=int)
parser.parse_args()

path = parser.path
start = parser.start
end = parse.end
stride = parser.stride

pipe = ovito.io.import_file(path, multiple_frames=True)
nframes = pipe.source.num_frames
if end==-10:
    end = nframes

for frame in range(start, end, stride):
    data = pipe.compute(frame)
    # only get x-y
    pos = data.particles.positions.array[:,:2]
    N = pos.shape[0]
    # count in each quadrant the number of particles
    quadrant_num = []
    for i in [-1,1]:
        for j in [-1, 1]:
            num  = (i*pos[:,0]>0)*(j*pos[:,1]>0)
            quadrant_num.append(num)
    print(quadrant_num)
    quadrant_num = np.array(quadrant_num)
    print(quadrant_num/N)
