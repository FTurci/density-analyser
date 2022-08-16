from analyser import Reader


class DensityField2d(Reader):
    """Project density and coarse grain over length dL"""
    def __init__(self):
        description = self.__doc__
        super().__init__(description)
        self.parser.add_argument(,"--dl",type=float, default=1.0)
        super().open_pipe()
