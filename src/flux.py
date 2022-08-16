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
        # print("skin",skin)
        # get initial positions
        data = self.pipe.compute(start)
        # only the x-component is important (the barrier is in the yz plane)
        pos_old = data.particles.positions.array[:,0]
        id_old =  data.particles.identifiers.array
        self.cell = data.cell[:]
        pos_old = pos_old[id_old.argsort()]
        id_old = id_old[id_old.argsort()]
        # take only particles that are close to the barrier (within a skin value)
        valid = (pos_old>-skin)*(pos_old<skin)
        # print(pos[valid])

        fout = open(self.path+f".flux.skin{skin}.txt","w")
        half_box =  self.cell[0,0]/2.
        for frame in range(start+1, end, stride):
            # print("po",pos[valid])
            data = self.pipe.compute(frame)
            pos = data.particles.positions.array[:,0]
            id =  data.particles.identifiers.array
            pos = pos[id.argsort()]
            id = id[id.argsort()]
            valid  =  valid *(np.absolute(pos-pos_old)<half_box)

            amax  = np.absolute(pos[valid]-pos_old[valid]).argmax()

            # print(id[valid][amax], id_old[valid][amax])
            # print((pos[valid]-pos_old[valid])[amax])
            sign_old = 2*(pos_old[valid]>0)-1.0
            sign = 2*(pos[valid]>0)-1.0
            # print(sign)
            # sign_switching = np.sum(sign!=sign_old)
            neg_to_pos = np.sum(sign>sign_old)
            pos_to_neg = np.sum(sign<sign_old)
            rest  = np.sum(sign==sign_old)
            fout.write(f"{frame} {neg_to_pos} {pos_to_neg}\n")
            pos_old =  pos.copy()
            id_old = id.copy()
            # update selection
            valid = (pos>-skin)*(pos<skin)



F = FluxMonitor()
F.compute()
