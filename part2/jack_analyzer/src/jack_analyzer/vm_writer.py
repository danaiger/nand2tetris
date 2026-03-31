import io
from typing import TextIO
from enum import Enum

class VMSegment(Enum):
    const= "constant"
    arg = "arg"
    local= "local"
    static = "static"
    this = "this"
    that = "that"
    pointer = "pointer"
    temp = "temp"


class VMWriter:
    def __init__(self, output_file: TextIO):
        self.output_file = output_file
    
    def write_function(self,name:str,n_locals:int):
        self.output_file.write(f"function {name} {n_locals}\n")
    
    def write_push(self,segment: VMSegment, index: int):
        self.output_file.write(f"push {segment.value} {index}\n")
    
    def write_return(self):
        self.output_file.write("return\n")


class NullVMWriter(VMWriter):
    def __init__(self):
        super().__init__(io.StringIO())
