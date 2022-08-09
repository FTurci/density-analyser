from analyser import Reader


class FluxMonitor(Reader):
    """Monitor flux of particles. Using argparse to parse arguments"":
    def __init__(self):
        description="Check the flow of particles across the barrier."
        super().__init__(description)
        super().open_pipe()

    def compute(self,skin = 5):
        start = self.args.start
        end = self.args.end
        stride = self.args.stride
        # get initial positions
        data = self.pipe.compute(frame)
        # only the x-component is important (the barrier is in the yz plane)
        pos_old = data.particles.positions.array[:,0]
        # take only particles that are close to the barrier (within a skin value)
        valid = (pos_old>-skin)+(pos_old<skin)
        sign_old = 2*(pos_old>0)-1.0
        for frame in range(start, end, stride):
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array[:,0]
            sign = 2*(pos>0)-1.0
            sign_swithing = np.sum(sign!=sign_old)
            print(sign_switching)


F = FluxMonitor()
