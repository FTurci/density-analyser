import ovito
import numpy as np
import argparse
import analyser

L = analyser.Lateral()
L.compute()
L.stats()
print(L.avg_profile)
