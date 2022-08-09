import ovito
import numpy as np
import argparse
import analyser

import os
L = analyser.LateralProfile()
L.compute()
# print(L.profiles)
L.stats(normalisation_density=0.45)

# os.environ["DISPLAY"] = "/private/tmp/com.apple.launchd.VxaBjzsSPo/org.xquartz:0"
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.plot(L.x,L.avg_rho_profile)
plt.savefig("fig.png")
