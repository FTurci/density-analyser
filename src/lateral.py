import ovito
import numpy as np
import argparse
from analyser import Quadrant

Q = Lateral("Analyse the density difference in the four quadrants of the plane orthogonal to z")
Q.compute()
