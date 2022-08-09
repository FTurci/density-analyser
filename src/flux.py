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
        data = self.pipe.compute(0)
        # only the x-component is important (the barrier is in the yz plane)
        pos_old = data.particles.positions.array[:,0]
        # take only particles that are close to the barrier (within a skin value)
        valid = (pos_old>-skin)+(pos_old<skin)
        sign_old = 2*(pos_old>0)-1.0
        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array[:,0]
            sign = 2*(pos>0)-1.0
            sign_switching = np.sum(sign!=sign_old)
            sign_old = sign.copy()
            print(frame, sign_switching)


F = FluxMonitor()
F.compute()
