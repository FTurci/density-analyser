from analyser import Reader
import numpy as np

class FluxMonitor(Reader):
    """Monitor flux of particles. Using argparse to parse arguments"""
    def __init__(self):
        description="Check the flow of particles across the barrier."
        super().__init__(description)
        self.parser.add_argument("-s","--skin",type=float, default=5.0)
        super().open_pipe()

    def compute(self):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        skin = self.args.skin
        # get initial positions
        data = self.pipe.compute(start)
        # only the x-component is important (the barrier is in the yz plane)
        pos_old = data.particles.positions.array[:,0]
        # take only particles that are close to the barrier (within a skin value)
        valid = (pos_old>-skin)+(pos_old<skin)
        sign_old = 2*(pos_old[valid]>0)-1.0
        for frame in range(start+1, end, stride):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array[:,0]
            # sign = 2*(pos[valid]>0)-1.0
            # # sign_switching = np.sum(sign!=sign_old)
            # neg_to_pos = np.sum(sign>sign_old)
            # pos_to_neg = np.sum(sign<sign_old)
            # rest  = np.sum(sign==sign_old)
            #
            # print(frame, neg_to_pos, pos_to_neg,rest,)
            # # update selection
            #
            # valid = (pos>-skin)+(pos<skin)
            # sign_old = 2*(pos[valid]>0)-1.0
            # del data


F = FluxMonitor()
F.compute()
