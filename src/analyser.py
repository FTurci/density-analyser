import ovito
import numpy as np
import argparse


class Reader:
    """Complete this generic reader in the furute!!!"""
    def __init__(self, description):
        pass


        parser = argparse.ArgumentParser(description)
        parser.add_argument("path",type=str)
        parser.add_argument("--start", default=0,type=int)
        parser.add_argument("--end", default=-10,type=int)
        parser.add_argument("--stride", default=1,type=int)
        self.args = parser.parse_args()

        self.pipe = ovito.io.import_file(self.args.path, multiple_frames=True)

        self.parser = parser
