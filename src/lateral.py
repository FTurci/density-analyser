import ovito
import numpy as np
import argparse
from analyser import Quadrant

L = Lateral()
L.compute()
L.stats()
print(L.avg_profile)
