from typing import TextIO

class VMWriter:
    def __init__(self, output_file: TextIO):
        self.output_file = output_file

class NullVMWriter(VMWriter):
    def __init__(self): pass
